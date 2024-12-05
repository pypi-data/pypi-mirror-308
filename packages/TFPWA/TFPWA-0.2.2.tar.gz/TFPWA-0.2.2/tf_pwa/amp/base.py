"""
Basic amplitude model
"""

import numpy as np

from tf_pwa.breit_wigner import (
    BW,
    BWR,
    BWR2,
    GS,
    Bprime,
    Bprime_polynomial,
    BWR_normal,
    Gamma,
)
from tf_pwa.breit_wigner import barrier_factor2 as barrier_factor
from tf_pwa.dec_parser import load_dec_file
from tf_pwa.dfun import get_D_matrix_lambda
from tf_pwa.particle import _spin_int, _spin_range
from tf_pwa.tensorflow_wrapper import tf

from .core import (
    AmpBase,
    AmpDecay,
    HelicityDecay,
    Particle,
    _ad_hoc,
    get_relative_p,
    get_relative_p2,
    regist_decay,
    regist_particle,
)


@regist_particle("BWR2")
class ParticleBWR2(Particle):
    """
        .. math::
            R(m) = \\frac{1}{m_0^2 - m^2 - i m_0 \\Gamma(m)}

        The difference of `BWR`, `BWR2` is the behavior when mass is below the threshold ( :math:`m_0 = 0.1 < 0.1 + 0.1 = m_1 + m_2`).


    .. plot::

        >>> import matplotlib.pyplot as plt
        >>> plt.clf()
        >>> from tf_pwa.utils import plot_particle_model
        >>> axis = plot_particle_model("BWR", {"mass": 0.1})
        >>> axis = plot_particle_model("BWR2", {"mass": 0.1}, axis=axis)
        >>> axis = plot_particle_model("BWR_below", {"mass": 0.1}, axis=axis)
        >>> axis = plot_particle_model("BWR_coupling", {"mass": 0.1}, axis=axis)
        >>> leg = axis[2].legend()

    """

    def get_amp(self, data, data_c, **kwargs):
        mass = self.get_mass()
        width = self.get_width()
        if width is None:
            return tf.ones_like(data["m"])
        if not self.running_width:
            ret = BW(data["m"], mass, width)
        else:
            q2 = data_c["|q|2"]
            q02 = data_c["|q0|2"]
            if self.bw_l is None:
                decay = self.decay[0]
                self.bw_l = min(decay.get_l_list())
            ret = BWR2(data["m"], mass, width, q2, q02, self.bw_l, self.d)
        return ret


@regist_particle("BWR_below")
class ParticleBWRBelowThreshold(Particle):
    """
    .. math::
        R(m) = \\frac{1}{m_0^2 - m^2 - i m_0 \\Gamma(m)}

    """

    def get_amp(self, data, data_c, **kwargs):
        mass = self.get_mass()
        width = self.get_width()
        q2 = data_c["|q|2"]
        decay = self.decay[0]
        _get_mass = lambda p: decay._get_particle_mass(p, data, False)

        m0 = mass
        m1 = _get_mass(decay.outs[0])
        m2 = _get_mass(decay.outs[1])
        m3 = _get_mass([i for i in self.creators[0].outs if i != self][0])
        m_eff = _ad_hoc(m0, _get_mass(self.creators[0].core) - m3, m1 + m2)
        m0 = tf.where(m0 < m1 + m2, m_eff, m0)
        q02 = get_relative_p2(m0, m1, m2)
        if self.bw_l is None:
            decay = self.decay[0]
            self.bw_l = min(decay.get_l_list())
        ret = BWR2(data["m"], mass, width, q2, q02, self.bw_l, self.d)
        return ret


@regist_particle("BWR_coupling")
class ParticleBWRCoupling(Particle):
    """

    Force :math:`q_0=1/d` to avoid below theshold condition for `BWR` model, and remove other constant parts, then the :math:`\\Gamma_0` is coupling parameters.

    .. math::
        R(m) = \\frac{1}{m_0^2 - m^2 - i m_0 \\Gamma_0 \\frac{q}{m} q^{2l} B_L'^2(q, 1/d, d)}

    .. plot::

        >>> import matplotlib.pyplot as plt
        >>> plt.clf()
        >>> from tf_pwa.utils import plot_particle_model
        >>> axis = plot_particle_model("BWR_coupling")

    """

    def get_amp(self, data, data_c, **kwargs):
        mass = self.get_mass()
        width = self.get_width()
        q2 = data_c["|q|2"]
        decay = self.decay[0]
        q02 = 1.0  # get_relative_p2(m0, m1, m2)
        if self.bw_l is None:
            decay = self.decay[0]
            self.bw_l = min(decay.get_l_list())
        normal = Bprime_polynomial(self.bw_l, 1.0)
        gamma = (
            tf.sqrt(q2)
            / data["m"]
            * q2**self.bw_l
            / Bprime_polynomial(self.bw_l, q2 * self.d**2)
        )
        a_r = mass**2 - data["m"] ** 2
        a_i = mass * width * gamma * tf.cast(normal, gamma.dtype)
        a_d = a_r * a_r + a_i * a_i
        ret = tf.complex(a_r / a_d, a_i / a_d)
        return ret

    def get_sympy_dom(self, m, m0, g0, m1=None, m2=None, sheet=0):
        from tf_pwa.formula import BWR_coupling_dom

        if self.bw_l is None:
            decay = self.decay[0]
            self.bw_l = min(decay.get_l_list())
        return BWR_coupling_dom(m, m0, g0, self.bw_l, m1, m2)


@regist_particle("BWR_normal")
class ParticleBWR_normal(Particle):
    """
    .. math::
        R(m) = \\frac{\\sqrt{m_0 \\Gamma(m)}}{m_0^2 - m^2 - i m_0 \\Gamma(m)}

    """

    def get_amp(self, data, data_c, **kwargs):
        mass = self.get_mass()
        width = self.get_width()
        if width is None:
            return tf.ones_like(data["m"])
        if not self.running_width:
            ret = BW(data["m"], mass, width)
        else:
            q2 = data_c["|q|2"]
            q02 = data_c["|q0|2"]
            if self.bw_l is None:
                decay = self.decay[0]
                self.bw_l = min(decay.get_l_list())
            ret = BWR_normal(
                data["m"], mass, width, q2, q02, self.bw_l, self.d
            )
        return ret


# added by xiexh for GS model rho
@regist_particle("GS_rho")
class ParticleGS(Particle):
    r"""
    Gounaris G.J., Sakurai J.J., Phys. Rev. Lett., 21 (1968), pp. 244-247

    `c_daug2Mass`: mass for daughter particle 2 (:math:`\pi^{+}`) 0.13957039

    `c_daug3Mass`: mass for daughter particle 3 (:math:`\pi^{0}`) 0.1349768

    .. math::
      R(m) = \frac{1 + D \Gamma_0 / m_0}{(m_0^2 -m^2) + f(m) - i m_0 \Gamma(m)}

    .. math::
      f(m) = \Gamma_0 \frac{m_0 ^2 }{q_0^3} \left[q^2 [h(m)-h(m_0)] + (m_0^2 - m^2) q_0^2 \frac{d h}{d m}|_{m0} \right]

    .. math::
      h(m) = \frac{2}{\pi} \frac{q}{m} \ln \left(\frac{m+2q}{2m_{\pi}} \right)

    .. math::
      \frac{d h}{d m}|_{m0} = h(m_0) [(8q_0^2)^{-1} - (2m_0^2)^{-1}] + (2\pi m_0^2)^{-1}

    .. math::
      D = \frac{f(0)}{\Gamma_0 m_0} = \frac{3}{\pi}\frac{m_\pi^2}{q_0^2} \ln \left(\frac{m_0 + 2q_0}{2 m_\pi }\right)
        + \frac{m_0}{2\pi q_0} - \frac{m_\pi^2 m_0}{\pi q_0^3}


    """

    def __init__(self, *args, **kwargs):
        self.c_daug2Mass = 0.13957039
        self.c_daug3Mass = 0.1349768
        super().__init__(*args, **kwargs)

    def get_amp(self, data, data_c, **kwargs):
        mass = self.get_mass()
        width = self.get_width()
        if width is None:
            return tf.ones_like(data["m"])
        if not self.running_width:
            ret = BW(data["m"], mass, width)
        else:
            q = data_c["|q|"]
            q0 = data_c["|q0|"]
            if self.bw_l is None:
                decay = self.decay[0]
                self.bw_l = min(decay.get_l_list())
            ret = GS(
                data["m"],
                mass,
                width,
                q,
                q0,
                self.bw_l,
                self.d,
                self.c_daug2Mass,
                self.c_daug3Mass,
            )
        return ret


# added by xiexh end


@regist_particle("BW")
class ParticleBW(Particle):
    """
        .. math::
            R(m) = \\frac{1}{m_0^2 - m^2 - i m_0 \\Gamma_0}

    .. plot::

        >>> import matplotlib.pyplot as plt
        >>> plt.clf()
        >>> from tf_pwa.utils import plot_particle_model
        >>> axis = plot_particle_model("BW")

    """

    def get_amp(self, data, _data_c=None, **kwargs):
        mass = self.get_mass()
        width = self.get_width()
        ret = BW(data["m"], mass, width)
        return ret

    def get_sympy_var(self):
        import sympy

        return sympy.var("m m0 g0")

    def get_num_var(self):
        mass = self.get_mass()
        width = self.get_width()
        return mass, width


@regist_particle("Kmatrix")
class ParticleKmatrix(Particle):
    def init_params(self):
        self.d = 3.0
        self.mass1 = self.add_var("mass1", fix=True)
        self.mass2 = self.add_var("mass2", fix=True)
        self.width1 = self.add_var("width1", fix=True)
        self.width2 = self.add_var("width2", fix=True)
        self.KNR = self.add_var("KNR", is_complex=True)
        self.alpha = self.add_var("alpha")
        self.beta0 = self.add_var("beta0", is_complex=True)
        self.beta1 = self.add_var("beta1", is_complex=True, fix=True)
        self.beta2 = self.add_var("beta2", is_complex=True)
        if self.bw_l is None:
            decay = self.decay[0]
            self.bw_l = min(decay.get_l_list())

    def get_amp(self, data, data_c=None, **kwargs):
        m = data["m"]
        mass1 = self.mass1()
        mass2 = self.mass2()
        width1 = self.width1()
        width2 = self.width2()
        q = data_c["|q|"]
        mdaughter1 = kwargs["all_data"]["particle"][self.decay[0].outs[0]]["m"]
        mdaughter2 = kwargs["all_data"]["particle"][self.decay[0].outs[1]]["m"]
        q1 = get_relative_p(mass1, mdaughter1, mdaughter2)
        q2 = get_relative_p(mass2, mdaughter1, mdaughter2)
        mlist = tf.stack([mass1, mass2])
        wlist = tf.stack([width1, width2])
        qlist = tf.stack([q1, q2])
        Klist = []
        for mi, wi, qi in zip(mlist, wlist, qlist):
            rw = Gamma(m, wi, q, qi, self.bw_l, mi, self.d)
            Klist.append(mi * rw / (mi**2 - m**2))
        KK = tf.reduce_sum(Klist, axis=0)
        KK += self.alpha()
        beta_term = self.get_beta(
            m=m,
            mlist=mlist,
            wlist=wlist,
            q=q,
            qlist=qlist,
            Klist=Klist,
            **kwargs,
        )
        MM = tf.complex(np.float64(1), -KK)
        MM = beta_term / MM
        return MM + self.KNR()

    def get_beta(self, m, **kwargs):
        m1, m2 = kwargs["mlist"]
        w1, w2 = kwargs["wlist"]
        q1, q2 = kwargs["qlist"]
        q = kwargs["q"]
        z = (q * self.d) ** 2
        z1 = (q1 * self.d) ** 2
        z2 = (q2 * self.d) ** 2
        Klist = kwargs["Klist"]
        beta1 = self.beta1()
        beta1 = beta1 * tf.cast(Klist[0] * m / m1 * q1 / q, beta1.dtype)
        beta1 = beta1 / tf.cast(
            (z / z1) ** self.bw_l * Bprime(self.bw_l, q, q1, self.d) ** 2,
            beta1.dtype,
        )
        beta2 = self.beta2()
        beta2 = beta2 * tf.cast(Klist[1] * m / m2 * q2 / q, beta2.dtype)
        beta2 = beta2 / tf.cast(
            (z / z2) ** self.bw_l * Bprime(self.bw_l, q, q2, self.d) ** 2,
            beta2.dtype,
        )
        beta0 = self.beta0()  # * tf.cast(2 * z / (z + 1), beta1.dtype)
        return beta0 + beta1 + beta2


@regist_particle("LASS")
class ParticleLass(Particle):
    def init_params(self):
        super(ParticleLass, self).init_params()
        self.a = self.add_var("a")
        self.r = self.add_var("r")

    def get_amp(self, data, data_c=None, **kwargs):
        r"""
        .. math::
          R(m) = \frac{m}{q cot \delta_B - i q}
            + e^{2i \delta_B}\frac{m_0 \Gamma_0 \frac{m_0}{q_0}}
                                  {(m_0^2 - m^2) - i m_0\Gamma_0 \frac{q}{m}\frac{m_0}{q_0}}

        .. math::
          cot \delta_B = \frac{1}{a q} + \frac{1}{2} r q

        .. math::
          e^{2i\delta_B} = \cos 2 \delta_B + i \sin 2\delta_B
                         = \frac{cot^2\delta_B -1 }{cot^2 \delta_B +1} + i \frac{2 cot \delta_B }{cot^2 \delta_B +1 }


        """
        m = data["m"]
        q = data_c["|q|"]
        q0 = data_c["|q0|"]
        mass = self.get_mass()
        width = self.get_width()
        a, r = tf.abs(self.a()), tf.abs(self.r())
        cot_delta_B = (1.0 / a) / q + 0.5 * r * q
        cot2_delta_B = cot_delta_B * cot_delta_B
        expi_2delta_B = tf.complex(cot2_delta_B - 1, 2 * cot_delta_B)
        expi_2delta_B /= tf.cast(cot2_delta_B + 1, expi_2delta_B.dtype)
        ret = 1.0 / tf.complex(q * cot_delta_B, -q)
        ret = tf.cast(m, ret.dtype) * ret
        ret += (
            expi_2delta_B
            * BWR(m, mass, width, q, q0, 0, 1.0)
            * tf.cast(mass * width * mass / q0, ret.dtype)
        )
        return ret


@regist_particle("one")
class ParticleOne(Particle):
    """
        .. math::
            R(m) = 1

    .. plot::

        >>> import  matplotlib.pyplot as plt
        >>> plt.clf()
        >>> from tf_pwa.utils import plot_particle_model
        >>> axis = plot_particle_model("one")
        >>> _ = axis[3].scatter([1.0],[0.0])

    """

    def init_params(self):
        pass

    def get_amp(self, data, _data_c=None, **kwargs):
        mass = data["m"]
        zeros = tf.zeros_like(mass)
        ones = tf.ones_like(mass)
        return tf.complex(ones, zeros)


@regist_particle("exp")
class ParticleExp(Particle):
    """
    .. math::
        R(m) = e^{-|a| m}

    """

    def init_params(self):
        self.a = self.add_var("a")

    def get_amp(self, data, _data_c=None, **kwargs):
        mass = data["m"]
        zeros = tf.zeros_like(mass)
        a = tf.abs(self.a())
        return tf.complex(tf.exp(-a * mass), zeros)


@regist_particle("exp_com")
class ParticleExpCom(Particle):
    """
    .. math::
        R(m) = e^{-(a+ib) m^2}

    lineshape when :math:`a=1.0, b=10.`

    .. plot::

        >>> import  matplotlib.pyplot as plt
        >>> plt.clf()
        >>> from tf_pwa.utils import plot_particle_model
        >>> axis = plot_particle_model("exp_com", plot_params={"R_BC_a": 1., "R_BC_b": 10.0})

    """

    def init_params(self):
        self.a = self.add_var("a")
        self.b = self.add_var("b")

    def get_amp(self, data, _data_c=None, **kwargs):
        mass = data["m"]
        zeros = tf.zeros_like(mass)
        a = self.a()
        b = self.b()
        r = -tf.complex(a, b) * tf.complex(mass * mass, zeros)
        return tf.exp(r)


@regist_particle("poly")
class ParticlePoly(Particle):
    """
    .. math::
        R(m) = \\sum c_i (m-m_0)^{n-i}

    lineshape when :math:`c_0=1, c_1=c_2=0`

    .. plot::

        >>> import  matplotlib.pyplot as plt
        >>> plt.clf()
        >>> from tf_pwa.utils import plot_particle_model
        >>> axis = plot_particle_model("poly", params={"n_order": 2}, plot_params={"R_BC_c_1r": 0., "R_BC_c_2r": 0., "R_BC_c_1i": 0., "R_BC_c_2i": 0.})

    """

    def init_params(self):
        self.n_order = getattr(self, "n_order", 3)
        self.pi = self.add_var("c", shape=(self.n_order + 1,), is_complex=True)
        self.pi.set_fix_idx(fix_idx=0, fix_vals=(1.0, 0.0))

    def get_amp(self, data, _data_c=None, **kwargs):
        mass = data["m"] - self.get_mass()
        pi = list(self.pi())
        mass = tf.complex(mass, tf.zeros_like(mass))
        return tf.math.polyval(pi, mass)


@regist_particle("MLP")
class ParticleMLP(Particle):
    """
    Multilayer Perceptron like model.

    .. math::
        R(m) = \\sum_{k} w_k activation(m-m_0+b_k)

    lineshape when `interp_N: 11`, `activation: relu`, :math:`b_k=(k-5)/10`, :math:`w_k = exp(k i\\pi/2)`

    .. plot::

        >>> import  matplotlib.pyplot as plt
        >>> import numpy as np
        >>> plt.clf()
        >>> from tf_pwa.utils import plot_particle_model
        >>> plot_params = {f"R_BC_b_{i}": (i-5)/10 for i in range(11)}
        >>> plot_params.update({f"R_BC_w_{i}r": 1 for i in range(11)})
        >>> plot_params.update({f"R_BC_w_{i}i": i * np.pi/2 for i in range(11)})
        >>> axis = plot_particle_model("MLP", params={"interp_N": 11, "activation": "relu"}, plot_params=plot_params)

    """

    activation_function = {
        "relu2": lambda x: tf.nn.relu(x) ** 2,
        "relu3": lambda x: tf.nn.relu(x) ** 3,
    }

    def init_params(self):
        self.interp_N = getattr(self, "interp_N", 3)
        self.activation = getattr(self, "activation", "leaky_relu")
        self.activation_f = ParticleMLP.activation_function.get(
            self.activation, getattr(tf.nn, self.activation)
        )
        self.bi = self.add_var("b", shape=(self.interp_N,))
        self.wi = self.add_var("w", shape=(self.interp_N,), is_complex=True)
        self.wi.set_fix_idx(fix_idx=0, fix_vals=(1.0, 0.0))

    def get_amp(self, data, _data_c=None, **kwargs):
        mass = data["m"] - self.get_mass()
        bi = tf.stack(self.bi())
        wi = tf.stack(self.wi())
        x = tf.expand_dims(mass, axis=-1) + bi
        x = self.activation_f(x)
        ret = tf.reduce_sum(wi * tf.complex(x, tf.zeros_like(x)), axis=-1)
        return ret


@regist_decay("particle-decay")
class ParticleDecay(HelicityDecay):
    def get_ls_amp(self, data, data_p, **kwargs):
        amp = super(ParticleDecay, self).get_ls_amp(data, data_p, **kwargs)
        a = self.core
        b = self.outs[0]
        c = self.outs[1]
        mass = a.get_mass()
        width = a.get_width()
        m = data_p[a]["m"]
        if width is None:
            ret = tf.zeros_like(m)
            ret = tf.complex(ret, ret)
        elif not a.running_width:
            ret = tf.reshape(BW(m, mass, width), (-1, 1))
        else:
            q = data["|q|"]
            q0 = data["|q0|"]
            ret = []
            for i in self.get_l_list():
                bw = BWR(m, mass, width, q, q0, i, self.d)
                ret.append(tf.reshape(bw, (-1, 1)))
            ret = tf.concat(ret, axis=-1)
        return ret * amp


@regist_decay("helicity_full")
class HelicityDecayNP(HelicityDecay):
    """
    Full helicity amplitude

    .. math::
        A = H_{m_1, m_2} D_{m_0, m_1-m_2}^{J_0 *}(\\varphi, \\theta,0)

    fit parameters is :math:`H_{m_1, m_2}`.

    """

    def init_params(self):
        a = self.outs[0].spins
        b = self.outs[1].spins
        self.H = self.add_var("H", is_complex=True, shape=(len(a), len(b)))
        self.fix_unused_h()

    def get_zero_index(self):
        a = self.outs[0].spins
        b = self.outs[1].spins
        fix_index = []
        free_index = []
        for idx_i, i in zip(range(self.H.shape[-2]), a):
            for idx_j, j in zip(range(self.H.shape[-1]), b):
                if abs(i - j) > self.core.J:
                    fix_index.append((idx_i, idx_j))
                else:
                    free_index.append((idx_i, idx_j))
        return fix_index, free_index

    def fix_unused_h(self):
        fix_index, free_idx = self.get_zero_index()
        self.H.set_fix_idx(fix_index, 0.0)
        self.H.set_fix_idx([free_idx[0]], 1.0)

    def get_H_zero_mask(self):
        fix_index, free_idx = self.get_zero_index()

    def get_factor(self):
        _, free_index = self.get_zero_index()
        H = self.H()
        return tf.gather_nd(H, free_index)

    def get_H(self):
        if self.mask_factor:
            H = tf.stack(self.H())
            _, free_idx = self.get_zero_index()
            return tf.scatter_nd(
                indices=free_idx,
                updates=tf.ones(len(free_idx), dtype=H.dtype),
                shape=H.shape,
            )
        return tf.stack(self.H())

    def get_helicity_amp(self, data=None, data_p=None, **kwargs):
        return self.get_H()

    def get_ls_amp(self, data, data_p, **kwargs):
        return tf.reshape(self.get_factor(), (1, -1))

    def get_factor_H(self, data=None, data_p=None, **kwargs):
        _, free_idx = self.get_zero_index()
        H = self.get_helicity_amp()
        value = tf.gather_nd(H, free_idx)
        new_idx = [(i, *j) for i, j in enumerate(free_idx)]
        return tf.scatter_nd(
            indices=new_idx, updates=value, shape=(len(free_idx), *H.shape)
        )


@regist_decay("helicity_full-bf")
class HelicityDecayNPbf(HelicityDecayNP):
    def init_params(self):
        self.d = 3.0
        super().init_params()

    def get_H_barrier_factor(self, data, data_p, **kwargs):
        q0 = self.get_relative_momentum(data_p, False)
        data["|q0|"] = q0
        if "|q|" in data:
            q = data["|q|"]
        else:
            q = self.get_relative_momentum(data_p, True)
            data["|q|"] = q
        bf = barrier_factor([min(self.get_l_list())], q, q0, self.d)
        return bf

    def get_helicity_amp(self, data, data_p, **kwargs):
        H = self.get_H()
        bf = self.get_H_barrier_factor(data, data_p, **kwargs)
        bf = tf.cast(tf.reshape(bf, (-1, 1, 1)), H.dtype)
        return H * bf

    def get_ls_amp(self, data, data_p, **kwargs):
        bf = self.get_H_barrier_factor(data, data_p, **kwargs)
        f = tf.reshape(self.get_factor(), (1, -1))
        return f * tf.expand_dims(tf.cast(bf, f.dtype), axis=-1)


def get_parity_term(j1, p1, j2, p2, j3, p3):
    p = p1 * p2 * p3 * (-1) ** (j1 - j2 - j3)
    return p


@regist_decay("helicity_parity")
class HelicityDecayP(HelicityDecayNP):
    """

    .. math::
        H_{- m1, - m2} = P_0 P_1 P_2 (-1)^{J_1 + J_2 - J_0} H_{m1, m2}

    """

    def init_params(self):
        a = self.core
        b = self.outs[0]
        c = self.outs[1]
        n_b = len(b.spins)
        n_c = len(c.spins)
        self.parity_term = get_parity_term(a.J, a.P, b.J, b.P, c.J, c.P)
        if n_b > n_c:
            self.H = self.add_var(
                "H", is_complex=True, shape=((n_b + 1) // 2, n_c)
            )
            self.part_H = 0
        else:
            self.H = self.add_var(
                "H", is_complex=True, shape=(n_b, (n_c + 1) // 2)
            )
            self.part_H = 1
        self.fix_unused_h()

    def get_helicity_amp(self, data, data_p, **kwargs):
        n_b = len(self.outs[0].spins)
        n_c = len(self.outs[1].spins)
        H_part = self.get_H()
        if self.part_H == 0:
            H = tf.concat(
                [
                    H_part,
                    self.parity_term * H_part[(n_b - 2) // 2 :: -1, ::-1],
                ],
                axis=0,
            )
        else:
            H = tf.concat(
                [
                    H_part,
                    self.parity_term * H_part[::-1, (n_c - 2) // 2 :: -1],
                ],
                axis=1,
            )
        return H


@regist_decay("gls-cpv")
class HelicityDecayCPV(HelicityDecay):
    """
    decay model for CPV
    """

    def init_params(self):
        self.d = 3.0
        ls = self.get_ls_list()
        self.g_ls = self.add_var(
            "g_ls", is_complex=True, shape=(len(ls),), is_cp=True
        )
        try:
            self.g_ls.set_fix_idx(fix_idx=0, fix_vals=(1.0, 0.0))
        except Exception as e:
            print(e, self, self.get_ls_list())

    def get_g_ls(self, charge=1):
        gls = self.g_ls(charge)
        if self.ls_index is None:
            return tf.stack(gls)
        # print(self, gls, self.ls_index)
        return tf.stack([gls[k] for k in self.ls_index])

    def get_ls_amp(self, data, data_p, **kwargs):
        charge = kwargs.get("all_data", {}).get("charge_conjugation", None)
        g_ls_p = self.get_g_ls(1)
        if charge is None:
            g_ls = g_ls_p
        else:
            g_ls_m = self.get_g_ls(-1)
            g_ls = tf.where((charge > 0)[:, None], g_ls_p, g_ls_m)
        # print(g_ls)
        q0 = self.get_relative_momentum2(data_p, False)
        data["|q0|2"] = q0
        if "|q|2" in data:
            q = data["|q|2"]
        else:
            q = self.get_relative_momentum2(data_p, True)
            data["|q|2"] = q
        if self.has_barrier_factor:
            bf = self.get_barrier_factor2(
                data_p[self.core]["m"], q, q0, self.d
            )
            mag = g_ls
            m_dep = mag * tf.cast(bf, mag.dtype)
        else:
            m_dep = g_ls
        return m_dep


@regist_decay("gls_reduce_h0")
class HelicityDecayReduceH0(HelicityDecay):
    """
    decay model that remove helicity =0 for massless particles
    """

    def init_params(self):
        self.d = 3.0

        all_hel, remove_hel = self.get_helicity_list2()
        ls = self.get_ls_list()

        self.g_ls = self.add_var(
            "g_ls",
            is_complex=True,
            shape=(len(ls) - len(remove_hel),),
            is_cp=True,
        )
        try:
            self.g_ls.set_fix_idx(fix_idx=0, fix_vals=(1.0, 0.0))
        except Exception as e:
            print(e, self, self.get_ls_list())

        all_matrix = self.get_cg_matrix()
        print(all_hel, remove_hel)

        matrix = []
        for i, j in remove_hel:
            idx_i = _spin_int(i + self.outs[0].J)
            idx_j = _spin_int(j + self.outs[1].J)
            matrix.append(all_matrix[:, idx_i, idx_j])
        # m g = h
        matrix = np.stack(matrix)
        # m_{zero,last} g_{last} + m_{zero, head} g_{head} = 0
        # m_{zero,last} g_{last} = - m_{zero,last}^{-1}  m_{zero, head} g_{head}
        matrix_inv = np.linalg.inv(matrix[:, -len(remove_hel) :])
        self.trans_matrix = (
            -np.dot(matrix_inv, matrix[:, : -len(remove_hel)]) + 0.0j
        )

    def get_helicity_list2(self):
        all_hel = []
        for i in _spin_range(-self.outs[0].J, self.outs[0].J):
            for j in _spin_range(-self.outs[1].J, self.outs[1].J):
                if abs(i - j) <= self.core.J:
                    if self.p_break or (-i, -j) not in all_hel:
                        all_hel.append((i, j))
        reduce_item = []
        for hi in all_hel:
            flag = False
            for p, k in zip(self.outs, hi):
                if p.get_mass() == 0 and k == 0:
                    flag = True
            if flag:
                reduce_item.append(hi)
        return all_hel, reduce_item

    def get_g_ls(self, charge=1):
        gls = self.g_ls(charge)
        gls = tf.stack(gls)
        gls_last = tf.linalg.matvec(self.trans_matrix, gls)
        gls = list(tf.unstack(gls)) + list(tf.unstack(gls_last))
        if self.ls_index is None:
            return tf.stack(gls)
        return tf.stack([gls[k] for k in self.ls_index])
