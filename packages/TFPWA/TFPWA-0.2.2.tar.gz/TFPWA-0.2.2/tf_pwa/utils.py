"""
This module provides some functions that may be useful in other modules.
"""

import functools
import json
import math
import time
import warnings

import numpy as np


class AttrDict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


has_yaml = True
try:
    import yaml
except ImportError:
    has_yaml = False


def _load_json_file(name):
    with open(name) as f:
        return json.load(f)


def _load_yaml_file(name):
    with open(name) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def create_dir(name):
    import os

    dirname = os.path.dirname(name)
    if dirname == "":
        return True
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)
        return False
    return True


def load_config_file(name):
    """
    Load config file such as **Resonances.yml**.

    :param name: File name. Either yml file or json file.
    :return: Dictionary read from the file.
    """
    if name.endswith("json"):
        return _load_json_file(name)
    if has_yaml:
        if name.endswith("yml"):
            return _load_yaml_file(name)
        return _load_yaml_file(name + ".yml")
    else:
        print("No yaml support, using json file")
        return _load_json_file(name + ".json")


def flatten_dict_data(data, fun="{}/{}".format):
    """
    Flatten nested dictionary data into one layer dictionary.

    :return: Dictionary
    """
    if isinstance(data, dict):
        ret = {}
        for i in data:
            tmp = flatten_dict_data(data[i])
            if isinstance(tmp, dict):
                for j in tmp:
                    ret[fun(i, j)] = tmp[j]
            else:
                ret[i] = tmp
        return ret
    else:
        return data


flatten_np_data = lambda data: flatten_dict_data(
    data, fun=lambda x, y: "{}{}".format(y, x[3:])
)


def error_print(x, err=None, dig=None):
    """
    It returns a format string "value +/- error". The precision is modified according to ``err``

    :param x: Value
    :param err: Error
    :return: String
    """
    if err is None:
        return ("{}").format(x)
    if err <= 0 or math.isnan(err):
        return ("{} ? {}").format(x, err)
    d = math.ceil(math.log10(err))
    b = 10**d
    b_err = err / b
    b_val = x / b
    if dig is None:
        if b_err < 0.355:  # 0.100 ~ 0.354
            dig = 2
        elif b_err < 0.950:  # 0.355 ~ 0.949
            dig = 1
        else:  # 0.950 ~ 0.999
            dig = 0
    err = round(b_err, dig) * b
    x = round(b_val, dig) * b
    d_p = dig - d
    if d_p > 0:
        return ("{0:.%df} +/- {1:.%df}" % (d_p, d_p)).format(x, err)
    return ("{0:.0f} +/- {1:.0f}").format(x, err)


def pprint(dicts):
    """
    Print dictionary using json format.
    """
    try:
        s = json.dumps(dicts, indent=2)
        print(s, flush=True)
    except:
        print(dicts, flush=True)


def print_dic(dic):
    """
    Another way to print dictionary.
    """
    if type(dic) == dict:
        for i in dic:
            print(i + " :\t", dic[i])
    else:
        print(dic)


def std_polar(rho, phi):
    """
    To standardize a polar variable. By standard form, it means :math:`\\rho>0, -\\pi<\\phi<\\pi`.

    :param rho: Real number
    :param phi: Real number
    :return: ``rho``, ``phi``
    """
    if rho < 0:
        rho = -rho
        phi += math.pi
    while phi < -math.pi:
        phi += 2 * math.pi
    while phi > math.pi:
        phi -= 2 * math.pi
    return rho, phi


def deep_iter(base, deep=1):
    for i in base:
        if deep == 1:
            yield [i]
        else:
            for j in deep_iter(base, deep - 1):
                yield [i] + j


def deep_ordered_iter(base, deep=1):
    ids = list(base)
    size = len(ids)
    for i in deep_ordered_range(size, deep):
        yield [ids[j] for j in i]


def deep_ordered_range(size, deep=1, start=0):
    for i in range(start, size):
        if deep <= 1:
            yield [i]
        else:
            for j in deep_ordered_range(size, deep - 1, i + 1):
                yield [i] + j


# from amplitude.py
def is_complex(x):
    """
    If **x** is of type ``complex``, it returns ``True``.
    """
    try:
        y = complex(x)
    except:
        return False
    return True


# from model.py
def array_split(data, batch=None):
    """Split a data array. **batch** is the number of data in a row."""
    if batch is None:
        return [data]
    ret = []
    n_data = data[0].shape[0]
    n_split = (n_data + batch - 1) // batch
    for i in range(n_split):
        tmp = []
        for data_i in data:
            tmp.append(data_i[i * batch : min(i * batch + batch, n_data)])
        ret.append(tmp)
    return ret


def time_print(f):
    """It provides a wrapper to print the time cost on a process."""

    @functools.wraps(f)
    def g(*args, **kwargs):
        now = time.time()
        ret = f(*args, **kwargs)
        print(f.__name__, " cost time:", time.time() - now)
        return ret

    return g


def std_periodic_var(p, mid=0.0, pi=math.pi):
    """
    Transform a periodic variable into its range.

    >>> std_periodic_var(math.pi)
    -3.1415...

    >>> std_periodic_var(2*math.pi + 0.01)
    0.0...

    :param p: Value
    :param mid: The middle value
    :param pi: Half-range
    :return: The transformed value
    """
    twopi = 2 * pi
    while p < mid - pi:
        p += twopi
    while p >= mid + pi:
        p -= twopi
    return p


def check_positive_definite(m):
    """check if matrix m is postive definite

    >>> check_positive_definite([[1.0,0.0],[0.0, 0.1]])
    True

    >>> check_positive_definite([[1.0,0.0],[1.0,-0.1]])
    eigvalues:  [-0.1  1. ]
    False

    """
    e, v = np.linalg.eig(m)
    if np.all(e > 0.0):
        return True
    warnings.warn("matrix is not positive definited")
    print("eigvalues: ", e)
    return False


def tuple_table(fit_frac, ignore_items=["sum_diag"]):
    names = []
    for i in fit_frac:
        if isinstance(i, str):
            names.append(i)
    for i in ignore_items:
        if i in names:
            names.remove(i)
    n_items = len(names)
    table = [[None] * (n_items + 1) for i in range(n_items + 1)]

    for k, v in fit_frac.items():
        if isinstance(k, tuple):
            a, b = k
            table[names.index(a) + 1][names.index(b) + 1] = v
        elif k in ignore_items:
            continue
        else:
            a, b = k, k
            table[names.index(a) + 1][names.index(b) + 1] = v

    for i, name in enumerate(names):
        table[i + 1][0] = name
        table[0][i + 1] = name

    return table


def save_frac_csv(file_name, fit_frac):
    import csv

    table = tuple_table(fit_frac)
    with open(file_name, "w") as f:
        f_csv = csv.writer(f)
        f_csv.writerows(table)


def fit_normal(data, weights=None):
    """
    Fit data distribution with Gaussian distribution. Though minimize the negative log likelihood function

    .. math::
        - \\ln L = \\frac{1}{2}\\sum w_i \\frac{(\\mu - x_i )^2}{\\sigma^2} + (\\sum w_i) \\ln (\\sqrt{2\pi} \\sigma )

    the fit result can be solved as

    .. math::
        \\frac{\\partial (-\\ln L)}{\\partial \\mu} = 0 \\Rightarrow \\bar{\\mu} = \\frac{\\sum w_i x_i}{ \\sigma^2 \\sum w_i}

    .. math::
        \\frac{\\partial (-\\ln L)}{\\partial \\sigma} = 0 \\Rightarrow \\bar{\\sigma} = \\sqrt{\\frac{\\sum w_i (\\bar{\\mu} - x_i)^2}{\\sum w_i}}

    From hessian

    .. math::
        \\frac{\\partial^2 (-\\ln L)}{\\partial \\mu^2} = \\frac{\\sum w_i}{\\sigma^2}

    .. math::
        \\frac{\\partial^2 (-\\ln L)}{\\partial \\sigma^2} = 3\\sum \\frac{\\sum w_i (\\mu - x)^2}{\\sigma^4} - \\frac{\\sum w_i}{\\sigma^2}

    the error matrix can wrotten as  [[ :math:`\\bar{\\sigma}^2/N` , 0], [0, :math:`\\bar{\\sigma}^2/(2N)` ]] .

    """
    if weights is None:
        weights = np.ones_like(data)
    else:
        weights = np.sum(weights) / np.sum(weights**2) * weights
    N = np.sum(weights)
    mu = np.sum(weights * data) / N
    sigma = np.sqrt(np.sum(weights * (data - mu) ** 2) / N)
    mu_error = sigma / np.sqrt(N)
    sigma_error = mu_error / np.sqrt(2)
    return np.array([mu, sigma]), np.array([mu_error, sigma_error])


def create_test_config(model_name, params={}, plot_params={}, top_mass=1.0):
    from tf_pwa.config_loader import ConfigLoader

    config_dic = {
        "data": {"dat_order": ["B", "C", "D"]},
        "decay": {"A": [["R_BC", "D"]], "R_BC": ["B", "C"]},
        "particle": {
            "$top": {"A": {"J": 0, "P": -1, "mass": top_mass}},
            "$finals": {
                "B": {"J": 0, "P": -1, "mass": 0.1},
                "C": {"J": 0, "P": -1, "mass": 0.1},
                "D": {"J": 0, "P": -1, "mass": 0.1},
            },
            "R_BC": {
                "J": 0,
                "P": +1,
                "mass": 0.5,
                "width": 0.05,
                "model": model_name,
            },
        },
    }
    config_dic["particle"]["R_BC"].update(params)
    config = ConfigLoader(config_dic)
    config.set_params({"A->R_BC.DR_BC->B.C_total_0r": 1.0})
    config.set_params({"A->R_BC.DR_BC->B.C_total_0i": 0.0})
    config.set_params(plot_params)
    return config


def plot_particle_model(
    model_name,
    params={},
    plot_params={},
    axis=None,
    special_points=None,
    mrange=(0.2, 0.9 - 1e-12),
):
    import matplotlib.pyplot as plt
    import numpy as np

    config = create_test_config(
        model_name, params, plot_params, top_mass=mrange[1] + 0.1 + 1e-12
    )
    f = config.get_particle_function("R_BC")
    m = np.linspace(mrange[0], mrange[1], 2000)
    a = f(m).numpy()
    if special_points is not None:
        special_points = np.array(special_points)
        at = f(special_points).numpy()
    if axis is None:
        ax3 = plt.subplot(2, 2, 3, label="argon")
        ax2 = plt.subplot(2, 2, 2, label="prob")
        ax1 = plt.subplot(2, 2, 1, sharex=ax3, label="real")
        ax0 = plt.subplot(2, 2, 4, sharex=ax2, sharey=ax3, label="imag")
    else:
        ax0, ax1, ax2, ax3 = axis
    ax3.plot(np.real(a), np.imag(a))
    if special_points is not None:
        ax3.scatter(np.real(at), np.imag(at))
    ax3.set_xlabel("Re$A$")
    ax3.set_ylabel("Im$A$")
    ax2.plot(m, np.abs(a) ** 2, label=model_name)
    if special_points is not None:
        ax2.scatter(special_points, np.abs(at) ** 2)
    ax2.set_ylabel("$|A|^2$")
    ax2.set_ylim((0, None))
    ax2.axvline(x=mrange[0], linestyle="--")
    ax2.yaxis.set_label_position("right")
    ax2.yaxis.tick_right()
    ax1.plot(np.real(a), m)
    if special_points is not None:
        ax1.scatter(np.real(at), special_points)
    ax1.set_ylabel("mass")
    ax0.plot(m, np.imag(a))
    if special_points is not None:
        ax0.scatter(special_points, np.imag(at))
    ax0.set_xlabel("mass")
    return [ax0, ax1, ax2, ax3]


def plot_pole_function(
    model_name, params={}, plot_params={}, axis=None, **kwargs
):
    import matplotlib.pyplot as plt
    import numpy as np

    config = create_test_config(model_name, params, plot_params)
    p = config.get_decay().get_particle("R_BC")
    f = p.pole_function()
    mx = np.linspace(0.2, 0.9 - 1e-12, 2000)
    my = np.linspace(-0.1, 0.1, 2000)
    a = np.abs(1 / f(mx + 1.0j * my[:, None])) ** 2
    if axis is None:
        axis = plt.gca()
    axis.contour(mx, my, a, linewidths=3)
    axis.set_xlabel("Re$\\sqrt{s}$")
    axis.set_ylabel("Im$\\sqrt{s}$")
    return axis


def search_interval(px, cl=0.6826894921370859, xrange=(0, 1)):
    """
    Search interval (a, b) that satisfly :math:`p(a)=p(b)` and

    .. math::
        \\frac{\\int_{a}^{b} p(x) dx}{\\int_{x_{min]}^{x_{max}} p(x) dx} = cl

    >>> x = np.linspace(-10, 10, 10000)
    >>> a, b = search_interval(np.exp(-x**2/2), xrange=(-10, 10))
    >>> assert abs(a+1) < 0.01
    >>> assert abs(b-1) < 0.01

    """
    n = px.shape[0]
    px = px / np.sum(px)
    idx = np.argsort(px)[::-1]
    y = px[idx]
    f = np.cumsum(y)
    cut = f < cl
    inner = idx[cut]
    left = (np.min(inner) - 1) / px.shape[0]
    right = (np.max(inner) + 1) / px.shape[0]
    a, b = xrange
    return a + (b - a) * left, a + (b - a) * right


def combine_asym_error(errs, N=10000):
    """

    combine asymmetry uncertanties using convolution

    >>> a, b = combine_asym_error([[-0.4, 0.4], 0.3])
    >>> assert abs(a+0.5) < 0.01
    >>> assert abs(b-0.5) < 0.01

    """
    from scipy.signal import convolve

    errs = [[i, i] if isinstance(i, float) else i for i in errs]
    errs = np.abs(np.stack(errs))
    max_range = np.max(np.sqrt(np.sum(errs**2, axis=0)))
    xrange = -max_range * 10, max_range * 10

    x = np.linspace(*xrange, N)

    y = np.exp(-(x**2) / 2 / np.where(x > 0, errs[-1, 1], errs[-1, 0]) ** 2)
    y = y / np.sum(y)
    for i in range(errs.shape[0] - 1):
        tmp = np.exp(
            -(x**2) / 2 / np.where(x > 0, errs[i, 1], errs[i, 0]) ** 2
        )
        tmp = tmp / np.sum(tmp)
        y = convolve(y, tmp, mode="same")
    return search_interval(y, xrange=xrange)
