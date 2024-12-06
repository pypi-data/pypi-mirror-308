"""
File to calculate the intensity map and broadening said map. and the velocity profile.
"""

from enum import Enum
from functools import partial
from typing import Literal, Tuple, Union

import jax
import jax.numpy as jnp
import numpy as np
from numba import njit


class RotationalBroadeningError(Exception):
    """Custom exception for rotational broadening calculation errors."""

    pass


ObservationType = Literal["emission", "transmission"]


@jax.jit
def calculate_velocity_step(wavelengths: jnp.ndarray) -> float:
    """Calculate the velocity step size from wavelength array."""
    delta_wavelengths = wavelengths[1:] - wavelengths[:-1]
    wavelength_means = (wavelengths[1:] + wavelengths[:-1]) / 2.0
    dRV = jnp.mean(2.0 * delta_wavelengths / wavelength_means) * 2.998e5
    return dRV


@jax.jit
def get_rotational_kernel(
    v_sin_i: Union[float, jnp.ndarray],
    wavelengths: jnp.ndarray,
    is_transmission: bool = False,
) -> jnp.ndarray:
    """
    Calculate rotational broadening kernel using JAX.

    Args:
        v_sin_i: Projected rotational velocity in km/s
        wavelengths: Array of wavelength points (must be sorted)
        is_transmission: If True, use transmission profile (1/pi/sqrt(1-x²)),
                        else emission profile (sqrt(1-x²))

    Returns:
        Normalized rotational broadening kernel
    """
    dRV = calculate_velocity_step(wavelengths)

    # Fixed kernel size for both modes
    indices = jnp.arange(401) - 200
    x_positions = indices * dRV / v_sin_i

    # Calculate profile based on observation mode
    profile = jnp.where(
        is_transmission,
        1.0 / (jnp.pi * jnp.sqrt(1 - x_positions**2)),  # transmission profile
        jnp.sqrt(1 - x_positions**2),  # emission profile
    )

    # Apply mask for valid regions (|x| < 1)
    kernel = jnp.where(jnp.abs(x_positions) < 1.0, profile, 0.0)

    # Normalize the kernel
    return kernel / jnp.sum(kernel)


def get_rot_ker(
    v_sin_i: Union[float, np.ndarray, jnp.ndarray],
    wavelengths: Union[np.ndarray, jnp.ndarray, list],
    observation: str = "emission",
) -> jnp.ndarray:
    """
    Safe wrapper for get_rotational_kernel with automatic array conversion.

    Args:
        v_sin_i: Projected rotational velocity in km/s
        wavelengths: Array of wavelength points
        observation: Type of observation, either "emission" or "transmission"

    Returns:
        Normalized kernel array

    Raises:
        RotationalBroadeningError: If calculation fails or if invalid observation type
    """
    # Validate observation type
    if observation not in ["emission", "transmission"]:
        raise RotationalBroadeningError(
            f"observation must be 'emission' or 'transmission', got '{observation}'"
        )

    try:
        # Convert inputs to JAX arrays if needed
        if not isinstance(wavelengths, jnp.ndarray):
            wavelengths = jnp.array(wavelengths)
        if isinstance(v_sin_i, (list, np.ndarray)):
            v_sin_i = jnp.array(v_sin_i)

        # Basic input validation
        if wavelengths.ndim != 1:
            raise RotationalBroadeningError(
                f"wavelengths must be 1D array, got shape {wavelengths.shape}"
            )
        if wavelengths.size < 2:
            raise RotationalBroadeningError(
                "wavelength array must have at least 2 points"
            )
        if isinstance(v_sin_i, (float, int)) and v_sin_i <= 0:
            raise RotationalBroadeningError(f"v_sin_i must be positive, got {v_sin_i}")

        # Calculate kernel
        kernel = get_rotational_kernel(
            v_sin_i, wavelengths, is_transmission=(observation == "transmission")
        )

        if jnp.any(jnp.isnan(kernel)):
            raise RotationalBroadeningError("Kernel calculation failed - check inputs")

        return kernel

    except Exception as e:
        if not isinstance(e, RotationalBroadeningError):
            raise RotationalBroadeningError(f"Calculation failed: {str(e)}")
        raise


# @njit
def get_theta(lat, lon):
    """
    Converts latitude and longitude to Theta, the angular distance across the disk.

    Inputs
    ------
        :lat: latitude in radians
        :lon: longitude in radians

    Outputs
    -------
        :res1: the angular distance across the disk.

    """
    if np.any(np.abs(lat) > np.pi) or np.any(np.abs(lon) > np.pi):
        raise ValueError("lat or lon is too large. are you inputting in radians?")
    else:
        return np.arccos(np.sqrt(1 - np.sin(lon) ** 2 - np.sin(lat) ** 2))


def fix_nan_result(res):
    """
    Fixes the result of a calculation that has NaNs in it.

    Parameters
    ----------
    res : float
        The result of a calculation.

    Returns
    -------
    float
        The result of the calculation with NaNs fixed.
    """
    if isinstance(res, np.ndarray) or isinstance(res, list):
        res[np.isnan(res)] = 0.0
    else:
        if np.isnan(res):
            res = 0.0
    return res


# @njit
def I_darken(lon, lat, epsilon):
    """
    takes lon and lat in. spits out the value on the limb-darkened disk.

    Inputs
    ------
        :lon: longitude in radians
        :lat: latitude in radians
        :epsilon: limb-darkening coefficient. should be between 0 and 1.

    Outputs
    -------
        :res1: the intensity at that point on the disk.
    """
    if 0.0 <= epsilon <= 1.0:
        theta = get_theta(lat, lon)
        res1 = (1 - epsilon) + (epsilon * np.cos(theta))

        res1 = fix_nan_result(res1)

        return res1
    else:
        raise ValueError("epsilon should only be from 0 to 1")


# @njit
def I_darken_disk(x, y, epsilon):
    """
    takes x and y in. spits out the value on the limb-darkened disk.

    Inputs
    ------
        :x: x position on the disk
        :y: y position on the disk
        :epsilon: limb-darkening coefficient. should be between 0 and 1.

    Outputs
    -------
        :res1: the intensity at that point on the disk.
    """
    lon = np.arcsin(x)
    lat = np.arcsin(y)

    return I_darken(lon, lat, epsilon)


def I_darken_disk_integrated(x, y, epsilon):
    """
    takes x and y in. spits out the value on the limb-darkened disk.

    Inputs
    ------
        :x: x position on the disk
        :y: y position on the disk
        :epsilon: limb-darkening coefficient. should be between 0 and 1.

    Outputs
    -------
        :res1: the intensity at that point on the disk.
    """
    lon = np.arcsin(x)
    lat = np.arcsin(y)

    dTheta = dx / np.cos(lon)
    dPhi = dy / np.cos(lat)

    return np.sum(
        dTheta * dPhi * np.cos(lon) * np.cos(lat) * I_darken(lon, lat, epsilon)
    )


@njit
def gaussian_term(lon, lat, offset, sigma, amp):
    """
    the gaussian term.

    Inputs
    ------
        :lat: latitude in radians
        :lon: longitude in radians
        :offset: the offset of the gaussian
        :sigma: the sigma of the gaussian
        :amp:  the amplitude of the gaussian

    Outputs
    -------
        :res1: the gaussian term.

    """
    return gaussian_term_1d(lat, 0.0, sigma, amp) * np.exp(
        -((lon - offset) ** 2) / (2 * sigma**2)
    )


@njit
def gaussian_term_1d(lat, offset, sigma, amp):
    """
    the gaussian term. this time there's no longitude dependence!

    Inputs
    ------
        :lat: latitude in radians
        :lon: longitude in radians
        :offset: the offset of the gaussian
        :sigma: the sigma of the gaussian
        :amp: the amplitude of the gaussian

    Outputs
    -------
        :res1: the gaussian term.
    """
    return (
        amp
        * (1 / (sigma**2 * 2 * np.pi))
        * np.exp(-((lat - offset) ** 2) / (2 * sigma**2))
    )


#### below: the actual integrations

vl = 1


@njit
def numerator_integral_no_sigma(vz, epsilon, n_samples=100):
    """
    calculates the numerator of the line profile. this is the version without the exponent.

    Parameters
    ----------
    vz : float
        The velocity of the star.
    epsilon : float
        The limb-darkening coefficient.
    n_samples : int
        The number of samples to use in the integration.

    Returns
    -------
    total_res : float
        The numerator of the line profile.
    """
    # set bounds
    lower_bound = 0
    upper_bound = np.arcsin(np.sqrt(1 - np.square(vz / vl)))
    # need to fix these bounds
    lat_arr = np.linspace(lower_bound, upper_bound, n_samples)
    d_lat = np.diff(lat_arr)[0]

    total_res = 0.0
    for lat in lat_arr:
        res = (
            (
                (1 - epsilon)
                + epsilon * np.sqrt(1 - np.square(vz / vl) - np.square(np.sin(lat)))
            )
            * np.cos(lat)
            * d_lat
        )
        if not np.isnan(res):
            total_res += res
    return total_res


@njit
def numerator_no_sigma(vz, epsilon, n_samples=100):
    """
    calculates the numerator of the line profile. this is the version without the exponent.

    Parameters
    ----------
    vz : float
        The velocity of the star.
    epsilon : float
        The limb-darkening coefficient.
    n_samples : int
        The number of samples to use in the integration.

    Returns
    -------
    res1 : float
        The numerator of the line profile.
    """
    res1 = 2
    return res1 * numerator_integral_no_sigma(vz, epsilon, n_samples=n_samples)


# @njit
def line_profile_no_exponent(epsilon, dRV, n_samples=int(1e4), model="igrins", vl=5):
    """
    calculates the line profile for a given epsilon and dRV. this is the version without the exponent.

    Parameters
    ----------
    epsilon : float
        The limb-darkening coefficient.
    dRV : float
        The width of the line profile.
    n_samples : int
        The number of samples to use in the integration.
    model : str
    vl : float
        The equatorial rotational velocity of the star.

    Returns
    -------
    big_resoluts : np.ndarray
        The line profile.

    """
    if model == "igrins":
        n_vz = 2 * vl / dRV
    else:
        n_vz = 500
    vzs = np.linspace(
        -1, 1, int(n_vz)
    )  # need to set to 0 if off disk. this is actually vz / vl. can also step off.
    big_resoluts = np.zeros(vzs.shape)

    for i, vz in enumerate(vzs):
        re_num = numerator_no_sigma(vz, epsilon, n_samples=n_samples)
        #         vz, epsilon, mu, sigma=.7, n_samples=100

        # todo: check sensitivity to lat / lon gridding
        re_denom = I_darken_disk_integrated(X, Y, epsilon)
        # pdb.set_trace()
        big_resoluts[i] = re_num / re_denom

    # normalize
    big_resoluts /= np.sum(big_resoluts)
    return big_resoluts


def convert_vz_to_lon(vz, R, sigma_jet, amp_jet, mu_jet):
    """
    Converts vz to a longitude.

    Parameters
    ----------
    vz : float
        The velocity along the line of sight.
    R : float
        The radius of the star.
    sigma_jet : float
        The width of the jet.
    amp_jet : float
        The amplitude of the jet.
    mu_jet : float
        The center of the jet.


    """
    gauss_term = gaussian_term_1d(vz, sigma_jet, amp_jet, mu_jet)
    return np.arcsin(vz / (R * gauss_term))


def convert_lon_to_vz(lon, R, sigma_jet, amp_jet, mu_jet):
    """
    Converts longitude to a vz

    Parameters
    ----------
    lon : float
        The longitude.
    R : float
        The radius of the planet.
    sigma_jet : float
        The width of the jet.
    amp_jet : float
        The amplitude of the jet.
    mu_jet : float
        The center of the jet.


    """
    vz = (
        R * np.sin(lon) * gaussian_term_1d(lon, sigma_jet, amp_jet, mu_jet)
    )  # todo: check another factor of R?
    return vz


# @njit
def broaden_spectrum(
    wav, spectrum_flux, epsilon, n_samples=int(1e4), vl=5, model="igrins"
):
    """
    Broadens a spectrum by a line profile.

    Parameters
    ----------
    wl_model : array-like
        The wavelength model.
    spectrum_flux : array-like
        The flux of the spectrum.
    epsilon : float
        The spot contrast.
    n_samples : int
        The number of samples to use in the integration.
    vl : float
        The rotational velocity of the object.

    Returns
    -------
    array-like
        The broadened spectrum.
    """
    # pdb.set_trace()
    dRV = (
        np.mean(
            np.array(
                [np.mean(np.diff(wav) / wav[1:]), np.mean(np.diff(wav) / wav[:-1])]
            )
        )
        * const_c
        / 1e3
    )
    profile = line_profile_no_exponent(
        epsilon, dRV, n_samples=n_samples, vl=vl, model=model
    )
    return np.convolve(spectrum_flux, profile, mode="same")


x = np.linspace(-1, 1, 80)
y = np.linspace(-1, 1, 80)

X, Y = np.meshgrid(x, y)

dx = np.diff(x)[0]
dy = np.diff(y)[0]

if __name__ == "__main__":
    x = np.linspace(-1, 1, 80)
    y = np.linspace(-1, 1, 80)

    vl = 5

    X, Y = np.meshgrid(x, y)

    dx = np.diff(x)[0]
    dy = np.diff(y)[0]

    lon = np.linspace(-90, 90, 80)
    lat = np.linspace(-90, 90, 80)

    lon = np.radians(lon)
    lat = np.radians(lat)

    LON, LAT = np.meshgrid(lon, lat)

    x = np.linspace(-1, 1, 80)
    y = np.linspace(-1, 1, 80)

    X, Y = np.meshgrid(x, y)

    res = I_darken(LON, LAT, 0.1)
    res_disk = I_darken_disk(X, Y, 0.9)
