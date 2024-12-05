import time

import numpy as np

from tf_pwa.generator import BaseGenerator, GenTest


class LinearInterp(BaseGenerator):
    """
    linear intepolation function for sampling
    """

    DataType = np.ndarray

    def __init__(self, x, y, epsilon=1e-10):
        self.x = x
        self.y = y
        self.N = x.shape[0]
        self.k = np.zeros((self.N - 1,))
        self.b = np.zeros((self.N - 1,))
        self.int_step = np.zeros((self.N - 1,))
        self.epsilon = epsilon
        self.int_all = 1.0
        self.cal_coeffs()

    def cal_coeffs(self):
        self.k = (self.y[1:] - self.y[:-1]) / (self.x[1:] - self.x[:-1])
        self.k = np.where(
            np.abs(self.k) > self.epsilon, self.k, np.zeros_like(self.k)
        )
        self.b = self.y[:-1] - self.k * self.x[:-1]
        int_x = 0.5 * self.k * (
            self.x[1:] ** 2 - self.x[:-1] ** 2
        ) + self.b * (self.x[1:] - self.x[:-1])
        self.int_step = np.cumsum(int_x)
        self.int_all = self.int_step[-1]

    def integral(self, x):
        bin_index = np.digitize(x, self.x[1:-1])
        k = self.k[bin_index]
        b = self.b[bin_index]
        x1 = self.x[1:][bin_index]
        d = self.int_step[bin_index]
        return 0.5 * k * (x * x - x1 * x1) + b * (x - x1) + d

    def generate(self, N):
        x = np.random.random(N)
        return self.solve(x)

    def solve(self, x):
        x = x * self.int_all
        bin_index = np.digitize(x, self.int_step[:-1])
        k = self.k[bin_index]
        b = self.b[bin_index]
        x1 = self.x[1:][bin_index]
        d = x - self.int_step[bin_index]
        y = np.sqrt(b**2 + k * (k * x1**2 + 2 * b * x1 + 2 * d)) - b
        y2 = d + b * x1
        return np.where(k == 0, y2, y) / np.where(k == 0, b, k)

    def __call__(self, x):
        bin_index = np.digitize(x, self.x[1:-1])
        k = self.k[bin_index]
        b = self.b[bin_index]
        return k * x + b


def interp_sample_f(f, f_interp, N):
    all_x = np.array([])
    max_rnd = None
    a = GenTest(100000000)
    for N2 in a.generate(N):
        x, max_rnd_new = interp_sample_once(f, f_interp, N2, max_rnd)
        if max_rnd is None:
            max_rnd = max_rnd_new
        if max_rnd_new > max_rnd:
            cut = np.random.random(all_x.shape[0]) > (
                1 - max_rnd / max_rnd_new
            )
            all_x = all_x[cut]
            a.set_gen(all_x.shape[0])
            max_rnd = max_rnd_new
        a.add_gen(x.shape[0])
        all_x = np.concatenate([all_x, x])
    # print("eff", a.eff, "extra", a.N_gen / N)
    return all_x[:N], f_interp, max_rnd


def interp_sample(f, xmin, xmax, interp_N, N):
    a = np.linspace(xmin, xmax, interp_N)
    b = f(a)
    f_interp = LinearInterp(a, b)
    return interp_sample_f(f, f_interp, N)


def interp_sample_once(f, f_interp, N, max_rnd):
    x = f_interp.generate(N)
    w = f(x) / f_interp(x)
    if max_rnd is None:
        max_rnd = np.max(w) * 1.02
    else:
        max_rnd = max(np.max(w) * 1.01, max_rnd)
    rnd = np.random.random(N) * max_rnd
    cut = w > rnd
    return x[cut], max_rnd


class LinearInterpImportance(BaseGenerator):
    DataType = np.ndarray

    def __init__(self, f, x):
        self.f = f
        self.x = x
        self.y = f(x)
        self.interp = LinearInterp(x, self.y)

    def __call__(self, x):
        return self.f(x)

    def generate(self, N):
        return interp_sample_f(self.f, self.interp, N)[0]


def sample_test_function(x):
    return np.abs(1 / (0.005 + (x - 1.5) ** 2)) + 200 * (x - 1.5) ** 2
