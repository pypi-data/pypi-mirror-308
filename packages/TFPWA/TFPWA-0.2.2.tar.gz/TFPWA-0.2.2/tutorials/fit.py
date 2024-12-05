import os.path
import sys

import numpy as np

this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, this_dir + "/..")

# import tf_pwa
from tf_pwa.config_loader import ConfigLoader
from tf_pwa.utils import error_print


def main():
    """Fit the amplitude model of data, calculating the fitting parameters and the fit fractions."""
    import argparse

    parser = argparse.ArgumentParser(
        description="a simple but complete analysis process"
    )
    parser.add_argument(
        "--final_params", default="final_params.json", dest="final_params"
    )
    results = parser.parse_args()

    fit(final_params_file=results.final_params)


def fit(final_params_file):
    # We use ConfigLoader to read the information in the configuration file
    config = ConfigLoader("config.yml")
    # Set init paramters. If not set, we will use random initial parameters
    # config.set_params("gen_params.json")
    fit_result = config.fit(method="BFGS")
    # calculate Hesse errors of the parameters
    errors = config.get_params_error(fit_result)
    print("\n########## fit parameters:")
    for key, value in config.get_params().items():
        print(key, error_print(value, errors.get(key, None)))
    # save fit_result to a json file
    fit_result.save_as(final_params_file)
    # Plot distributions of variables indicated in the configuration file
    config.plot_partial_wave(fit_result)

    fit_frac, err_frac = config.cal_fitfractions()
    print("\n########## fit fractions:")
    for i in fit_frac:
        if not isinstance(i, tuple):  # fit fraction
            name = i
        else:
            name = "{}x{}".format(*i)  # interference term
        print(name + ": " + error_print(fit_frac[i], err_frac.get(i, None)))


if __name__ == "__main__":
    main()
