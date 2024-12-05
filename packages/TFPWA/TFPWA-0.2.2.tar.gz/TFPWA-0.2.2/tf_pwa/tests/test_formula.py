import numpy as np
import tensorflow as tf

from tf_pwa.amp import get_decay, get_particle
from tf_pwa.amp.split_ls import get_relative_p2


def simple_decay(name, **extra):
    a = get_particle(
        name, J=1, P=-1, model=name, mass=3.6, width=0.01, **extra
    )
    b = get_particle("b", mass=0.5, J=0, P=-1)
    c = get_particle("c", mass=0.5, J=0, P=-1)
    decay = get_decay(a, [b, c])
    a.init_params()
    decay.init_params()
    return a


def nest_dict_zip(a, b):
    ret = {}
    for i, j in zip(a, b):
        if isinstance(i, (list, tuple)):
            tmp = nest_dict_zip(i, j)
        else:
            tmp = {i: j}
        ret.update(tmp)
    return ret


def simple_test(model, **extra):
    p = simple_decay(model, **extra)
    p.solve_pole()
    m = np.array([3.5, 3.6, 3.7])
    a = 1 / p(m).numpy()
    var = p.get_sympy_var()
    f = p.get_sympy_dom(*var)
    g = f.subs(nest_dict_zip(var[1:], p.get_num_var()))
    b = np.array([complex(g.subs({var[0]: i}).evalf()) for i in m])
    assert np.allclose(np.real(a), np.real(b))
    assert np.allclose(np.imag(a), np.imag(b))


def test_BW():
    simple_test("BW")


def test_BWR():
    simple_test("BWR")


def test_coupling():
    simple_test("BWR_coupling")


def run_BWR_LS(**extra):
    p = simple_decay("BWR_LS", **extra)
    p.solve_pole()
    m = np.array([3.5, 3.6, 3.7])
    var = p.get_sympy_var()
    f = p.get_sympy_dom(*var)
    var_num = p.get_num_var()
    g = f.subs(nest_dict_zip(var[1:], var_num))
    b = np.array([complex(g.subs({var[0]: i}).evalf()) for i in m])

    q = get_relative_p2(m, *var_num[-2:])
    q0 = get_relative_p2(3.6, *var_num[-2:])
    a, _ = p.get_ls_amp_frac(m, p.decay[0].get_ls_list(), q, q0)
    assert np.allclose(np.real(a.numpy()), np.real(b))
    assert np.allclose(np.imag(a.numpy()), np.imag(b))


def test_BWR_LS():
    run_BWR_LS()
    run_BWR_LS(fix_bug1=True)


def test_grad():
    p = simple_decay("BWR_LS")
    p.mass.freed()
    with p.mass.vm.error_trans(None) as pm:
        a = p.solve_pole()
        b = tf.math.real(a)
        c = tf.math.imag(a)
    pm.get_grad(b, keep=True)
    pm.get_grad(c)


def test_grad2():
    p = simple_decay("BWR")
    p.mass.freed()
    with p.mass.vm.error_trans(None) as pm:
        a = p.solve_pole()
        b, c = tf.math.real(a), tf.math.imag(a)
    pm.get_grad(b, keep=True)
    pm.get_grad(c)


def test_flatte_pole():
    p = simple_decay("FlatteC", mass_list=[[0.1, 0.1], [0.3, 0.3]])
    p.mass.freed()
    p.mass.vm.set("FlatteC_g_0", 0.3)
    p.mass.vm.set("FlatteC_g_1", 0.4)
    with p.mass.vm.error_trans(None) as pm:
        b, c = p.solve_pole(init=3.6 - 0.05j, return_complex=False, sheet=1)
    pm.get_grad(b, keep=True)
    pm.get_grad(c)


def flatte2_pole_temp(**kwargs):
    p = simple_decay(
        "Flatte2", mass_list=[[0.1, 0.1], [0.3, 0.3]], l_list=[0, 1], **kwargs
    )
    p.mass.freed()
    p.mass.vm.set("Flatte2_g_0", 0.3)
    p.mass.vm.set("Flatte2_g_1", 0.4)
    with p.mass.vm.error_trans(None) as pm:
        b, c = p.solve_pole(init=3.6 - 0.05j, return_complex=False, sheet=1)
    ga = pm.get_grad(b, keep=True)
    gc = pm.get_grad(c)


def test_flatte2_pole():
    flatte2_pole_temp(cut_phsp=True)
    flatte2_pole_temp(no_q0=True)
    flatte2_pole_temp(no_m0=True)
    flatte2_pole_temp(has_bprime=True)


def test_flatte2_width():
    p = simple_decay(
        "Flatte2", mass_list=[[0.1, 0.1], [0.3, 0.3]], g_0=0.3, float=["g_0"]
    )
    p.mass.freed()
    p.mass.vm.set("Flatte2_g_0", 0.3)
    p.mass.vm.set("Flatte2_g_1", 0.4)
    p.solve_pole()
    width = p.get_width()
    width = p.get_width(np.array([3.6]))
