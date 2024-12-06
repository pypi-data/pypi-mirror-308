Installation
-------------
To install `scope`, you can use `pip`::

    pip install scope

To install from source, run::

    python3 -m pip install -U pip
    python3 -m pip install -U setuptools setuptools_scm pep517
    git clone https://github.com/arjunsavel/scope
    cd scope
    python3 -m pip install -e .

All of the required dependencies will be installed automatically. Our current list of dependencies
(which will be pruned by v1.0.0) is:

* https://github.com/numpy/numpy
* https://github.com/astropy/astropy
* https://github.com/scipy/scipy
* https://github.com/pandas-dev/pandas
* https://github.com/matplotlib/matplotlib
* https://github.com/adrn/schwimmbad
* https://github.com/google/jax
* https://github.com/numba/numba
* https://github.com/dfm/emcee
* https://github.com/pymc-devs/pymc
* https://github.com/scikit-learn/scikit-learn
* https://github.com/exoplanet-dev/exoplanet
* https://github.com/tqdm/tqdm


In the future, we plan to release `scope` on conda.
