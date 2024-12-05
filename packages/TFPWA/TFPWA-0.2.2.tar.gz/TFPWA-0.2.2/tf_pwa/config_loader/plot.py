import itertools
import os

import matplotlib.pyplot as plt
import numpy as np
import sympy as sym
import yaml

from tf_pwa.adaptive_bins import AdaptiveBound
from tf_pwa.adaptive_bins import cal_chi2 as cal_chi2_o
from tf_pwa.data import (
    batch_call,
    batch_call_numpy,
    data_index,
    data_merge,
    data_replace,
    data_shape,
    data_split,
    data_to_numpy,
    load_data,
    save_data,
)
from tf_pwa.histogram import Hist1D, interp_hist
from tf_pwa.root_io import has_uproot, save_dict_to_root

from .config_loader import ConfigLoader, validate_file_name


def _reverse(gen, idx):
    for i in gen:
        yield [i[j] for j in idx]


def default_color_generator(color_first):
    colors = [
        "red",
        "orange",
        "purple",
        "springgreen",
        "y",
        "green",
        "blue",
        "c",
    ]
    linestyles = ["-", "--", "-.", ":"]
    marker = [",", ".", "^"]
    if color_first:
        style = itertools.product(marker, linestyles, colors)
    else:
        style = _reverse(
            itertools.product(marker, colors, linestyles), (0, 2, 1)
        )
    return style


class LineStyleSet:
    def __init__(self, file_name, color_first=True):
        self.file_name = file_name
        self.linestyle_table = None
        if file_name is not None and os.path.exists(file_name):
            with open(file_name) as f:
                self.linestyle_table = yaml.full_load(f)
        if self.linestyle_table is None:
            self.linestyle_table = []
        self.linestyle_generator = default_color_generator(color_first)
        self.style_key = ["label", "linestyle", "marker", "color"]

    def get(self, id_, default=None):
        id_ = str(id_)
        used_linestyle = []
        for i in self.linestyle_table:
            if i["id"] == id_:
                return i
            used_linestyle.append((i["marker"], i["linestyle"], i["color"]))
        if default is not None:
            self.linestyle_table.append({"id": id_, **default})
            return default
        for i in self.linestyle_generator:
            if i in used_linestyle:
                continue
            marker, line, color = i
            item = {
                "id": id_,
                "color": color,
                "linestyle": line,
                "marker": marker,
            }
            self.linestyle_table.append(item)
            return item
        return None

    def get_style(self, id_):
        style = self.get(id_)
        style_key = self.style_key
        return {k: v for k, v in style.items() if k in style_key}

    def save(self):
        if self.file_name is None:
            return
        with open(self.file_name, "w") as f:
            yaml.dump(self.linestyle_table, f)


def _get_cfit_bg(self, data, phsp, batch=65000):
    model = self._get_model()
    bg_function = [i.bg for i in model]
    w_bkg = [i.w_bkg for i in model]
    phsp_weight = []
    for data_i, phsp_i, w, bg_f in zip(data, phsp, w_bkg, bg_function):
        ndata = np.sum(data_i.get_weight())
        nbg = ndata * w
        w_bg = batch_call_numpy(bg_f, phsp_i, batch) * phsp_i.get_weight()
        phsp_weight.append(-w_bg / np.sum(w_bg) * nbg)
    ret = [
        data_replace(phsp_i, "weight", w)
        for phsp_i, w in zip(phsp, phsp_weight)
    ]
    return ret


def _get_cfit_eff_phsp(self, phsp, batch=65000):
    model = self._get_model()
    eff_function = [i.eff for i in model]
    phsp_weight = []
    for phsp_i, eff_f in zip(phsp, eff_function):
        w_eff = batch_call_numpy(eff_f, phsp_i, batch) * phsp_i.get_weight()
        phsp_weight.append(w_eff)

    ret = [
        data_replace(phsp_i, "weight", w)
        for phsp_i, w in zip(phsp, phsp_weight)
    ]
    return ret


@ConfigLoader.register_function()
def get_chain_property(self, idx, display=True):
    """Get chain name and curve style in plot"""
    chain = self.get_chain(idx)
    chains_id_method = self.chains_id_method
    if chains_id_method == "auto":
        if len(list(chain)) <= 3:
            chains_id_method = "first_decay"
        else:
            chains_id_method = "res"
    if "res" not in self.chains_id_method_table:
        self.chains_id_method_table["res"] = get_chain_property_v2
    if "first_decay" not in self.chains_id_method_table:
        self.chains_id_method_table["first_decay"] = get_chain_property_v1
    f = self.chains_id_method_table[chains_id_method]
    return f(self, idx, display)


def get_chain_property_v1(self, idx, display):
    chain = self.get_chain(idx)
    for i in chain:
        curve_style = i.curve_style
        break
    combine = []
    for i in chain:
        if i.core == chain.top:
            combine = list(i.outs)
    names = []
    displays = []
    for i in combine:
        pro = self.particle_property[str(i)]
        names.append(str(i))
        displays.append(pro.get("display", str(i)))
    if display:
        return " ".join(displays), curve_style
    return "_".join(names), curve_style


def get_chain_property_v2(self, idx, display):
    chain = self.get_chain(idx)
    for i in chain:
        curve_style = i.curve_style
        break
    all_res = chain.inner
    combine = []
    # sorted with the decay order
    for i in chain:
        if i.core in all_res:
            combine.append(i.core)
    names = []
    displays = []
    for i in combine:
        pro = self.particle_property[str(i)]
        names.append(str(i))
        displays.append(pro.get("display", str(i)))
    if display:
        return "/".join(displays), curve_style
    return "_".join(names), curve_style


def create_chain_property(self, res):
    chain_property = []
    pro = self.particle_property
    res2str = lambda x: pro.get(str(x), {}).get("display", str(x))
    if res is None:
        for i in range(len(self.full_decay.chains)):
            name_i, curve_style = self.get_chain_property(i, False)
            label, curve_style = self.get_chain_property(i, True)
            chain_property.append([i, name_i, label, curve_style])
    else:
        for i, name in enumerate(res):
            if not isinstance(name, list):
                name = [name]
            if len(name) == 1:
                display = res2str(name[0])
            else:
                display = (
                    "{ " + ",\n  ".join([res2str(i) for i in name]) + " }"
                )
            name_i = "_".join([str(i) for i in name])
            chain_property.append([i, name_i, display, None])
    return chain_property


def create_plot_var_dic(plot_params, extra_plots=None):
    extra_plots = [] if extra_plots is None else extra_plots
    plot_var_dic = {}
    common_bins = None
    for conf in plot_params.get_params() + extra_plots:
        name = conf.get("name")
        display = conf.get("display", name)
        upper_ylim = conf.get("upper_ylim", None)
        idx = conf.get("idx", (None,))
        trans = conf.get("trans", lambda x: x)
        readdata = conf.get("readdata")
        has_legend = conf.get("legend", False)
        xrange = conf.get("range", None)
        bins = conf.get("bins", common_bins)
        if common_bins is None:
            common_bins = bins
        legend_outside = conf.get("legend_outside", False)
        units = conf.get("units", "")
        yscale = conf.get("yscale", "linear")
        plot_var_dic[name] = {
            "display": display,
            "upper_ylim": upper_ylim,
            "legend": has_legend,
            "legend_outside": legend_outside,
            "idx": idx,
            "trans": trans,
            "readdata": readdata,
            "range": xrange,
            "bins": bins,
            "units": units,
            "yscale": yscale,
        }
    return plot_var_dic


@ConfigLoader.register_function()
def plot_partial_wave(
    self,
    params=None,
    data=None,
    phsp=None,
    bg=None,
    prefix="figure/",
    res=None,
    save_root=False,
    chains_id_method=None,
    phsp_rec=None,
    cut_function=lambda x: 1,
    plot_function=None,
    **kwargs
):
    """
    plot partial wave plots

    :param self: ConfigLoader object
    :param params: params, dict or FitResutls
    :param data: data sample, a list of CalAngleData
    :param phsp: phase space sample, a list of CalAngleData (the same size as data)
    :param bg: background sample, a list of CalAngleData (the same size as data)
    :param prefix: figure saving folder and nameing prefix
    :param res: combination of resonaces in partial wave, list of (list of (string for resoances name or int for decay chain index))
    :param save_root: if save weights in a root file, bool
    :param chains_id_method: method of how legend label display, string

    :param bin_scale: more binning in partial waves for a smooth histogram. int
    :param batch: batching in calculating weights, int

    :param smooth: if plot smooth binned kde shape or histogram, bool
    :param single_legend: if save all legend in a file "legend.pdf", bool
    :param plot_pull: if plot the pull distribution, bool
    :param format: save figure with image format, string (such as ".png", ".jpeg")
    :param linestyle_file: legend linestyle configuration file name (YAML format), string (such as "legend.yml")

    """
    if plot_function is None:
        plot_function = self._plot_partial_wave

    path = os.path.dirname(prefix)
    os.makedirs(path, exist_ok=True)

    all_plot_data = self._get_plot_partial_wave_input(
        params=params,
        data=data,
        phsp=phsp,
        bg=bg,
        prefix=prefix,
        res=res,
        save_root=save_root,
        chains_id_method=chains_id_method,
        phsp_rec=phsp_rec,
        cut_function=cut_function,
        **kwargs,
    )

    for i, all_data in enumerate(all_plot_data):
        data_dict, phsp_dict, bg_dict = all_data[0]
        prefix, plot_var_dic, chain_property, nll = all_data[1]
        plot_function(
            data_dict,
            phsp_dict,
            bg_dict,
            prefix=prefix,
            plot_var_dic=plot_var_dic,
            chain_property=chain_property,
            nll=nll,
            **kwargs,
        )


@ConfigLoader.register_function()
def plot_partial_wave_interf(self, res1, res2, **kwargs):

    labels = ["data"]
    if self.config["data"].get("model", "auto") == "cfit":
        labels.append("background")
    elif self.config["data"].get("bg", None) is not None:
        labels.append("background")

    if kwargs.get("ref_amp", None) is not None:
        labels.append("reference fit")
    labels.append("total fit")

    if kwargs.get("force_legend_labels", None) is not None:
        labels = kwargs["force_legend_labels"]
        del kwargs["force_legend_labels"]

    labels += [str(res1), str(res2), "sum", "interference"]

    if not isinstance(res1, list):
        res1 = [res1]
    if not isinstance(res2, list):
        res2 = [res2]

    amp = self.get_amplitude()

    def weights_function(data, **kwargs):
        with amp.temp_used_res(res1):
            a = amp(data)
        with amp.temp_used_res(res2):
            b = amp(data)
        with amp.temp_used_res(res1 + res2):
            ab = amp(data)
        return [a, b, ab, ab - a - b]

    self.plot_partial_wave(
        partial_waves_function=weights_function,
        force_legend_labels=labels,
        **kwargs,
    )


@ConfigLoader.register_function()
def _get_plot_partial_wave_input(
    self,
    params=None,
    data=None,
    phsp=None,
    bg=None,
    prefix="figure/",
    res=None,
    phsp_rec=None,
    save_root=False,
    chains_id_method=None,
    cut_function=lambda x: 1,
    partial_waves_function=None,
    extra_plots=None,
    **kwargs
):
    """
    plot partial wave plots

    :param self: ConfigLoader object
    :param params: params, dict or FitResutls
    :param data: data sample, a list of CalAngleData
    :param phsp: phase space sample, a list of CalAngleData (the same size as data)
    :param bg: background sample, a list of CalAngleData (the same size as data)
    :param prefix: figure saving folder and nameing prefix
    :param res: combination of resonaces in partial wave, list of (list of (string for resoances name or int for decay chain index))
    :param save_root: if save weights in a root file, bool
    :param chains_id_method: method of how legend label display, string

    :param bin_scale: more binning in partial waves for a smooth histogram. int
    :param batch: batching in calculating weights, int

    :param smooth: if plot smooth binned kde shape or histogram, bool
    :param single_legend: if save all legend in a file "legend.pdf", bool
    :param plot_pull: if plot the pull distribution, bool
    :param format: save figure with image format, string (such as ".png", ".jpeg")
    :param linestyle_file: legend linestyle configuration file name (YAML format), string (such as "legend.yml")

    """
    if params is None:
        params = {}
    nll = None
    if hasattr(params, "min_nll"):
        nll = float(getattr(params, "min_nll"))
    if hasattr(params, "params"):
        params = getattr(params, "params")
    # print(nll, params)
    path = os.path.dirname(prefix)
    os.makedirs(path, exist_ok=True)

    if data is None:
        data = self.get_data_rec("data")
        bg = self.get_data_rec("bg")
        phsp = self.get_phsp_plot()
        phsp_rec = self.get_phsp_plot("_rec")
    phsp_rec = phsp if phsp_rec is None else phsp_rec
    batch = kwargs.get("batch", 65000)
    if bg is None:
        if self.config["data"].get("model", "auto") == "cfit":
            bg = _get_cfit_bg(self, data, phsp, batch)
        else:
            bg = [bg] * len(data)
    if self.config["data"].get("model", "auto") == "cfit":
        phsp = _get_cfit_eff_phsp(self, phsp, batch)
        phsp_rec = _get_cfit_eff_phsp(self, phsp_rec, batch)
    amp = self.get_amplitude()
    self._Ngroup = len(data)
    ws_bkg = [
        None if bg_i is None else bg_i.get("weight", None) for bg_i in bg
    ]
    # ws_bkg, ws_inmc = self._get_bg_weight(data, bg)
    if chains_id_method is not None:
        self.chains_id_method = chains_id_method

    if partial_waves_function is None:
        chain_property = create_chain_property(self, res)
    else:
        chain_property = [
            [i, "pw_{}".format(i), "partial waves {}".format(i), None]
            for i in range(100)
        ]
    plot_var_dic = create_plot_var_dic(
        self.plot_params, extra_plots=extra_plots
    )

    if self._Ngroup == 1:
        data_dict, phsp_dict, bg_dict = self._cal_partial_wave(
            amp,
            params,
            data[0],
            phsp[0],
            bg[0],
            ws_bkg[0],
            prefix,
            plot_var_dic,
            chain_property,
            save_root=save_root,
            res=res,
            phsp_rec=phsp_rec[0],
            cut_function=cut_function,
            partial_waves_function=partial_waves_function,
            **kwargs,
        )
        all_data = data_dict, phsp_dict, bg_dict
        extra = prefix, plot_var_dic, chain_property, nll
        yield all_data, extra
    else:
        combine_plot = self.config["plot"].get("combine_plot", True)
        if not combine_plot:
            for dt, mc, sb, w_bkg, i in zip(
                data, phsp, bg, ws_bkg, range(self._Ngroup)
            ):
                data_dict, phsp_dict, bg_dict = self._cal_partial_wave(
                    amp,
                    params,
                    dt,
                    mc,
                    sb,
                    w_bkg,
                    prefix + "d{}_".format(i),
                    plot_var_dic,
                    chain_property,
                    save_root=save_root,
                    phsp_rec=phsp_rec[i],
                    cut_function=cut_function,
                    partial_waves_function=partial_waves_function,
                    **kwargs,
                )
                all_data = data_dict, phsp_dict, bg_dict
                extra = (
                    prefix + "d{}_".format(i),
                    plot_var_dic,
                    chain_property,
                    nll,
                )
                yield all_data, extra
        else:
            for dt, mc, sb, w_bkg, i in zip(
                data, phsp, bg, ws_bkg, range(self._Ngroup)
            ):
                data_dict, phsp_dict, bg_dict = self._cal_partial_wave(
                    amp,
                    params,
                    dt,
                    mc,
                    sb,
                    w_bkg,
                    prefix + "d{}_".format(i),
                    plot_var_dic,
                    chain_property,
                    save_root=save_root,
                    res=res,
                    phsp_rec=phsp_rec[i],
                    cut_function=cut_function,
                    partial_waves_function=partial_waves_function,
                    **kwargs,
                )
                # self._plot_partial_wave(data_dict, phsp_dict, bg_dict, path+'d{}_'.format(i), plot_var_dic, chain_property, **kwargs)
                if i == 0:
                    datas_dict = {}
                    for ct in data_dict:
                        datas_dict[ct] = [data_dict[ct]]
                    phsps_dict = {}
                    for ct in phsp_dict:
                        phsps_dict[ct] = [phsp_dict[ct]]
                    bgs_dict = {}
                    for ct in bg_dict:
                        bgs_dict[ct] = [bg_dict[ct]]
                else:
                    for ct in data_dict:
                        datas_dict[ct].append(data_dict[ct])
                    for ct in phsp_dict:
                        phsps_dict[ct].append(phsp_dict[ct])
                    for ct in bg_dict:
                        bgs_dict[ct].append(bg_dict[ct])
            for ct in datas_dict:
                datas_dict[ct] = np.concatenate(datas_dict[ct])
            for ct in phsps_dict:
                phsps_dict[ct] = np.concatenate(phsps_dict[ct])
            for ct in bgs_dict:
                bgs_dict[ct] = np.concatenate(bgs_dict[ct])
            if has_uproot and save_root:
                if not bgs_dict:
                    save_dict_to_root(
                        [datas_dict, phsps_dict],
                        file_name=prefix + "variables_com.root",
                        tree_name=["data", "fitted"],
                    )
                else:
                    save_dict_to_root(
                        [datas_dict, phsps_dict, bgs_dict],
                        file_name=prefix + "variables_com.root",
                        tree_name=["data", "fitted", "sideband"],
                    )
                print("Save root file " + prefix + "com_variables.root")

            all_data = datas_dict, phsps_dict, bgs_dict
            extra = prefix + "com_", plot_var_dic, chain_property, nll
            yield all_data, extra


@ConfigLoader.register_function()
def _cal_partial_wave(
    self,
    amp,
    params,
    data,
    phsp,
    bg,
    w_bkg,
    prefix,
    plot_var_dic,
    chain_property,
    save_root=False,
    bin_scale=3,
    res=None,
    batch=65000,
    ref_amp=None,
    phsp_rec=None,
    cut_function=lambda x: 1,
    partial_waves_function=None,
    **kwargs
):
    data_dict = {}
    phsp_dict = {}
    bg_dict = {}
    phsp_rec = phsp if phsp_rec is None else phsp_rec

    resolution_size_phsp = data_shape(phsp) // data_shape(phsp_rec)
    sr = lambda w: np.sum(
        np.reshape(data_to_numpy(w), (-1, resolution_size_phsp)), axis=-1
    )
    with amp.temp_params(params):
        weight_phsp = batch_call_numpy(
            amp, phsp, batch
        )  # (i) for i in data_split(phsp, batch)]
        # weight_phsp = data_merge(*weights_i)
        phsp_origin_w = phsp.get("weight", 1.0) * phsp.get("eff_value", 1.0)
        total_weight = sr(weight_phsp * phsp_origin_w)
        if ref_amp is not None:
            # weights_i_ref = [ref_amp(i) for i in data_split(phsp, batch)]
            weight_phsp_ref = batch_call_numpy(
                ref_amp, phsp, batch
            )  # data_merge(*weights_i_ref)
            total_weight_ref = sr(weight_phsp_ref * phsp_origin_w)
        data_weight = data.get("weight", None)
        if data_weight is None:
            n_data = data_shape(data)
        else:
            n_data = np.sum(data_weight)
        if bg is None:
            norm_frac = n_data / np.sum(total_weight)
            if ref_amp is not None:
                norm_frac_ref = n_data / np.sum(total_weight_ref)
        else:
            n_sig = n_data + np.sum(w_bkg)
            norm_frac = n_sig / np.sum(total_weight)
            if ref_amp is not None:
                norm_frac_ref = n_sig / np.sum(total_weight_ref)
        if partial_waves_function is None:
            weights = batch_call_numpy(
                lambda x: amp.partial_weight(x, combine=res), phsp, batch
            )
        else:
            weights = batch_call_numpy(
                lambda x: partial_waves_function(x, combine=res), phsp, batch
            )
        data_weights = data.get("weight", np.ones((data_shape(data),)))
        data_dict["data_weights"] = (
            batch_call_numpy(cut_function, data, batch) * data_weights
        )
        phsp_weights = total_weight * norm_frac
        cut_phsp = batch_call_numpy(cut_function, phsp_rec, batch)
        phsp_dict["MC_total_fit"] = cut_phsp * phsp_weights  # MC total weight

        if ref_amp is not None:
            phsp_dict["MC_total_fit_ref"] = (
                cut_phsp * total_weight_ref * norm_frac_ref
            )
        if bg is not None:
            bg_weight = -w_bkg
            # sideband weight
            bg_dict["sideband_weights"] = (
                batch_call_numpy(cut_function, bg, batch) * bg_weight
            )
        for i, name_i, label, _ in chain_property:
            if i >= len(weights):
                break
            weight_i = (
                weights[i]
                * norm_frac
                * bin_scale
                * phsp.get("weight", 1.0)
                * phsp.get("eff_value", 1.0)
            )
            # MC partial weight
            phsp_dict["MC_{0}_{1}_fit".format(i, name_i)] = cut_phsp * sr(
                weight_i
            )
        for name in plot_var_dic:
            readdata = plot_var_dic[name]["readdata"]
            idx = plot_var_dic[name].get("idx", (None,))

            data_i = batch_call_numpy(readdata, data, batch)
            if idx[-1] == "m":
                tmp_idx = list(idx)
                tmp_idx[-1] = "p"
                p4 = batch_call_numpy(
                    lambda x: data_index(x, tmp_idx, no_raise=True),
                    data,
                    batch,
                )
                if p4 is not None:
                    p4 = np.transpose(p4)
                    data_dict[name + "_E"] = p4[0]
                    data_dict[name + "_PX"] = p4[1]
                    data_dict[name + "_PY"] = p4[2]
                    data_dict[name + "_PZ"] = p4[3]
            data_dict[name] = data_i  # data variable

            phsp_i = batch_call_numpy(readdata, phsp_rec, batch)
            phsp_dict[name + "_MC"] = phsp_i  # MC

            if bg is not None:
                bg_i = batch_call_numpy(readdata, bg, batch)
                bg_dict[name + "_sideband"] = bg_i  # sideband
    data_dict = data_to_numpy(data_dict)
    phsp_dict = data_to_numpy(phsp_dict)
    bg_dict = data_to_numpy(bg_dict)
    if has_uproot and save_root:
        if bg is None:
            save_dict_to_root(
                [data_dict, phsp_dict],
                file_name=prefix + "variables.root",
                tree_name=["data", "fitted"],
            )
        else:
            save_dict_to_root(
                [data_dict, phsp_dict, bg_dict],
                file_name=prefix + "variables.root",
                tree_name=["data", "fitted", "sideband"],
            )
        print("Save root file " + prefix + "variables.root")
    return data_dict, phsp_dict, bg_dict


@ConfigLoader.register_function()
def _plot_partial_wave(
    self,
    data_dict,
    phsp_dict,
    bg_dict,
    prefix,
    plot_var_dic,
    chain_property,
    plot_delta=False,
    plot_pull=False,
    save_pdf=False,
    bin_scale=3,
    single_legend=False,
    format="png",
    nll=None,
    smooth=True,
    linestyle_file=None,
    color_first=True,
    ref_amp=None,
    add_chi2=False,
    dpi=300,
    force_legend_labels=None,
    labels=None,
    **kwargs
):
    # cmap = plt.get_cmap("jet")
    # N = 10
    # colors = [cmap(float(i) / (N+1)) for i in range(1, N+1)]

    style = LineStyleSet(linestyle_file, color_first=color_first)

    data_weights = data_dict["data_weights"]
    if bg_dict:
        bg_weight = bg_dict["sideband_weights"]
    phsp_weights = phsp_dict["MC_total_fit"]
    for name in plot_var_dic:
        if not name in data_dict:
            continue
        data_i = data_dict[name]
        phsp_i = phsp_dict[name + "_MC"]
        if bg_dict:
            bg_i = bg_dict[name + "_sideband"]

        display = plot_var_dic[name]["display"]
        upper_ylim = plot_var_dic[name]["upper_ylim"]
        has_legend = plot_var_dic[name]["legend"]
        legend_outside = plot_var_dic[name]["legend_outside"]
        bins = plot_var_dic[name]["bins"]
        units = plot_var_dic[name]["units"]
        xrange = plot_var_dic[name]["range"]
        yscale = plot_var_dic[name].get("yscale", "linear")
        if xrange is None:
            xrange = [np.min(data_i) - 0.1, np.max(data_i) + 0.1]
        # data_x, data_y, data_err = hist_error(
        # data_i, bins=bins, weights=data_weights, xrange=xrange
        # )
        data_cut = data_weights != 0
        data_hist = Hist1D.histogram(
            data_i[data_cut],
            weights=data_weights[data_cut],
            range=xrange,
            bins=bins,
        )
        fig = plt.figure()
        if plot_delta or plot_pull:
            if legend_outside and has_legend:
                ax = plt.subplot2grid((4, 6), (0, 0), rowspan=3, colspan=5)
            else:
                ax = plt.subplot2grid((4, 1), (0, 0), rowspan=3)
        else:
            if legend_outside and has_legend:
                ax = plt.subplot2grid((4, 6), (0, 0), rowspan=4, colspan=5)
            else:
                ax = fig.add_subplot(1, 1, 1)

        legends = []
        legends_label = []
        has_negative = False

        le = data_hist.draw_error(
            ax, fmt=".", zorder=-2, label="data", color="black"
        )
        has_negative = has_negative and np.any(data_hist.count < 0)

        legends.append(le)
        legends_label.append("data")

        fitted_hist = Hist1D.histogram(
            phsp_i, weights=phsp_weights, range=xrange, bins=bins
        )
        if ref_amp is not None:
            fitted_hist_ref = Hist1D.histogram(
                phsp_i,
                weights=phsp_dict["MC_total_fit_ref"],
                range=xrange,
                bins=bins,
            )

        if bg_dict:
            bg_hist = Hist1D.histogram(
                bg_i,
                weights=bg_weight,
                range=xrange,
                bins=bins,
                mask_error=1,
            )
            le = bg_hist.draw_bar(
                ax, label="back ground", alpha=0.5, color="grey"
            )
            has_negative = has_negative or np.any(bg_hist.count < 0)
            fitted_hist = fitted_hist + bg_hist
            if ref_amp is not None:
                fitted_hist_ref = fitted_hist_ref + bg_hist
            legends.append(le)
            legends_label.append("back ground")
        if ref_amp is not None:
            le2 = fitted_hist_ref.draw(
                ax, label="reference fit", color="red", linewidth=2
            )
            has_negative = has_negative or np.any(fitted_hist_ref.count < 0)
            legends.append(le2[0])
            legends_label.append("reference fit")
        le2 = fitted_hist.draw(ax, label="total fit", color="black")
        has_negative = has_negative or np.any(fitted_hist.count < 0)
        legends.append(le2[0])
        legends_label.append("total fit")

        for i, name_i, label, curve_style in chain_property:
            idx_name = "MC_{0}_{1}_fit".format(i, name_i)
            if idx_name not in phsp_dict:
                continue
            weight_i = phsp_dict[idx_name]
            if np.allclose(weight_i, 0):
                continue
            hist_i = Hist1D.histogram(
                phsp_i,
                weights=weight_i,
                range=xrange,
                bins=bins * bin_scale,
            )
            if smooth:
                if curve_style is None:
                    line = style.get_style(name_i)
                    label = line.get("label", label)
                    line["label"] = label
                    kwargs = {"linewidth": 1, **line}
                    # marker, ls, color = line["marker"], line["linestyle"], line["color"]
                    le3 = hist_i.draw_kde(ax, **kwargs)
                else:
                    le3 = hist_i.draw_kde(
                        ax, fmt=curve_style, label=label, linewidth=1
                    )
            else:
                if curve_style is None:
                    line = style.get_style(name_i)
                    label = line.get("label", label)
                    line["label"] = label
                    kwargs = {"linewidth": 1, **line}
                    # marker, ls, color = line["marker"], line["linestyle"], line["color"]
                    le3 = hist_i.draw(ax, **kwargs)
                else:
                    le3 = hist_i.draw(
                        ax,
                        color=curve_style[0],
                        linestyle=curve_style[1:],
                        label=label,
                        linewidth=1,
                    )

            has_negative = has_negative or np.any(hist_i.count < 0)
            legends.append(le3[0])
            legends_label.append(label)
        if yscale == "log":
            ax.set_ylim((0.1, upper_ylim))
        else:
            if has_negative:
                ax.set_ylim((None, upper_ylim))
            else:
                ax.set_ylim((0, upper_ylim))
        ax.set_xlim(xrange)
        ax.set_yscale(yscale)
        if force_legend_labels:
            legends_label = force_legend_labels
        if has_legend:
            if labels is not None:
                legends_label = labels
            if legend_outside:
                leg = ax.legend(
                    legends,
                    legends_label,
                    frameon=False,
                    fontsize="small",
                    labelspacing=0.1,
                    borderpad=0.0,
                    bbox_to_anchor=(1.02, 0.5),
                    loc=6,
                )
            else:
                leg = ax.legend(
                    legends,
                    legends_label,
                    frameon=False,
                    labelspacing=0.1,
                    borderpad=0.0,
                )
        if nll is None:
            ax.set_title(display, fontsize="xx-large")
        else:
            ax.set_title(
                "{}: -lnL= {:.2f}".format(display, nll), fontsize="xx-large"
            )
        ax.set_xlabel(display + units)
        ywidth = np.mean(
            data_hist.bin_width
        )  # (max(data_x) - min(data_x)) / bins
        ax.set_ylabel("Events/{:.3f}{}".format(ywidth, units))
        diff_hist = data_hist - fitted_hist
        chi2_ax = ax
        if plot_delta or plot_pull:
            plt.setp(ax.get_xticklabels(), visible=False)
            if legend_outside and has_legend:
                ax2 = plt.subplot2grid((4, 6), (3, 0), rowspan=1, colspan=5)
            else:
                ax2 = plt.subplot2grid((4, 1), (3, 0), rowspan=1)
            chi2_ax = ax2

            # y_err = fit_y - data_y
            # if plot_pull:
            # _epsilon = 1e-10
            # with np.errstate(divide="ignore", invalid="ignore"):
            # fit_err = np.sqrt(fit_y)
            # y_err = y_err / fit_err
            # y_err[fit_err < _epsilon] = 0.0
            # ax2.bar(data_x, y_err, color="k", alpha=0.7, width=ywidth)
            if plot_pull:
                diff_hist.draw_pull()
                ax2.axhline(y=0, color="r", linewidth=0.5)
                ax2.axhline(
                    y=3,
                    color="r",
                    linestyle="--",
                    linewidth=0.5,
                )
                ax2.axhline(
                    y=-3,
                    color="r",
                    linestyle="--",
                    linewidth=0.5,
                )
                ax2.set_ylabel("pull")
                ax2.set_ylim((-5, 5))
            else:
                diff_hist.draw_bar(color="grey")
                ax2.set_ylabel("$\\Delta$Events")
                y_err = diff_hist.count
                ax2.set_ylim((-max(abs(y_err)), max(abs(y_err))))
            ax.set_xlabel("")
            ax2.set_xlabel(display + units)
            if xrange is not None:
                ax2.set_xlim(xrange)

        if add_chi2:
            chi2_ax.text(
                0,
                1,
                "$\\chi^2/Nbins={:.2f}/{:}$".format(
                    diff_hist.chi2(), diff_hist.ndf()
                ),
                ha="left",
                va="top",
                transform=chi2_ax.transAxes,
            )
        # ax.set_yscale("log")
        # ax.set_ylim([0.1, 1e3])
        fig.savefig(prefix + name + "." + format, dpi=dpi)
        if single_legend:
            export_legend(ax, prefix + "legend.{}".format(format))
        if save_pdf:
            fig.savefig(prefix + name + ".pdf", dpi=dpi)
            if single_legend:
                export_legend(ax, prefix + "legend.pdf")
        print("Finish plotting " + prefix + name)
        plt.close(fig)

    style.save()

    self._2d_plot_v2(
        data_dict,
        phsp_dict,
        bg_dict,
        prefix,
        plot_var_dic,
        chain_property,
        plot_delta=plot_delta,
        plot_pull=plot_pull,
        save_pdf=save_pdf,
        bin_scale=bin_scale,
        single_legend=single_legend,
        format=format,
        nll=nll,
        smooth=smooth,
        color_first=color_first,
        **kwargs,
    )


def _plot_var_name(name):
    if isinstance(name, (list, tuple)):
        sub = name[0]
        if sub == "mass":
            assert len(name) == 2, str(name)
            return "m_" + name[1]
        if sub == "angle":
            assert len(name) == 3
            return validate_file_name(name[1] + "_" + name[2])
        if sub == "aligned_angle":
            assert len(name) == 3
            return "aligned_" + validate_file_name(name[1] + "_" + name[2])
    if isinstance(name, str):
        return name
    raise TypeError("not string or list")


def build_read_var_function(all_var, where={}):
    vari = [sym.simplify(i) for i in all_var]
    used_var = []
    var_index = []
    all_symbols = set()
    for i in vari:
        all_symbols = all_symbols | i.free_symbols
    all_symbols = tuple(all_symbols)

    for i in all_symbols:
        var_index.append(str(i))
        used_var.append(where.get(str(i), str(i)))

    used_var = [_plot_var_name(i) for i in used_var]

    def get_var(dic, tail):
        ret = []
        for i in used_var:
            ret.append(dic[i + tail])
        return dict(zip(var_index, ret))

    var_f = [sym.lambdify(all_symbols, i, modules="numpy") for i in vari]
    return var_f, get_var


@ConfigLoader.register_function()
def _2d_plot_v2(
    self,
    data_dict,
    phsp_dict,
    bg_dict,
    prefix,
    plot_var_dic,
    chain_property,
    plot_delta=False,
    plot_pull=False,
    save_pdf=False,
    bin_scale=3,
    single_legend=False,
    format="png",
    nll=None,
    smooth=True,
    color_first=True,
    **kwargs
):
    twodplot = self.config["plot"].get("2Dplot", {})
    new_plot = {}
    for k, v in twodplot.items():
        if "&" in k:
            var1, var2 = k.split("&")
            var1 = var1.rstrip()
            var2 = var2.lstrip()
            k = var1 + "_vs_" + var2
            v["x"] = var1
            v["y"] = var2
            if (
                "xrange" not in v
                and var1 in plot_var_dic
                and "range" in plot_var_dic[var1]
            ):
                v["xrange"] = plot_var_dic[var1]["range"]
            if (
                "yrange" not in v
                and var2 in plot_var_dic
                and "range" in plot_var_dic[var2]
            ):
                v["yrange"] = plot_var_dic[var2]["range"]
            if "vs" in v.get("display", ""):
                name1, name2 = v.get("display", "").split("vs")
                name1 = name1.rstrip()
                name2 = name2.lstrip()
                if "xlabel" not in v:
                    v["xlabel"] = name1
                if "ylabel" not in v:
                    v["ylabel"] = name2
            new_plot[k] = v
    twodplot.update(new_plot)
    for k, v in twodplot.items():
        if "&" in k:
            continue
        assert ("x" in v) and ("y" in v)

        var_x = sym.simplify(v["x"])
        var_y = sym.simplify(v["y"])
        where = v.get("where", {})

        (var_x_f, var_y_f), get_var = build_read_var_function(
            [var_x, var_y], where
        )

        data_1 = var_x_f(**get_var(data_dict, ""))
        data_2 = var_y_f(**get_var(data_dict, ""))
        phsp_1 = var_x_f(**get_var(phsp_dict, "_MC"))
        phsp_2 = var_y_f(**get_var(phsp_dict, "_MC"))

        x_range = v.get("xrange", None)
        if x_range is None:
            x_range = [np.min(phsp_1) - 0.1, np.max(phsp_1) + 0.1]
        y_range = v.get("yrange", None)
        if y_range is None:
            y_range = [np.min(phsp_2) - 0.1, np.max(phsp_2) + 0.1]

        x_bins = v.get("xbins", 100)
        y_bins = v.get("ybins", 100)

        display = v.get("display", k)
        title = display

        plot_figs = v.get("plot_figs", ["data", "sidbanand", "fitted"])
        name1 = v.get("xlabel", str(var_x))
        name2 = v.get("ylabel", str(var_y))

        def plot_axis():
            plt.xlabel(name1)
            plt.ylabel(name2)
            plt.xlim(x_range)
            plt.ylim(y_range)

        plt.clf()
        # data
        if "data" in plot_figs:
            cut = data_dict["data_weights"] != 0
            plt.scatter(data_1[cut], data_2[cut], s=1, alpha=0.8, label="data")
            plot_axis()
            plt.title(title, fontsize="xx-large")
            plt.savefig(prefix + k + "_data")
            plt.clf()
            print("Finish plotting 2D data " + prefix + k)
        if "data_hist" in plot_figs:
            plt.hist2d(
                data_1,
                data_2,
                bins=[x_bins, y_bins],
                weights=data_dict["data_weights"],
                range=[x_range, y_range],
                cmin=1e-12,
            )
            plot_axis()
            plt.title(title, fontsize="xx-large")
            plt.colorbar()
            plt.savefig(prefix + k + "_data_hist")
            plt.clf()
            print("Finish plotting 2D data_hist " + prefix + k)
        # sideband
        if "sideband" in plot_figs:
            if bg_dict:
                bg_1 = var_x_f(**get_var(bg_dict, "_sideband"))
                bg_2 = var_y_f(**get_var(bg_dict, "_sideband"))
                plt.scatter(
                    bg_1, bg_2, s=1, c="g", alpha=0.8, label="sideband"
                )
                plot_axis()
                plt.title(title, fontsize="xx-large")
                plt.savefig(prefix + k + "_bkg")
                plt.clf()
                print("Finish plotting 2D sideband " + prefix + k)
            else:
                print("There's no bkg input")
        if "sideband_hist" in plot_figs:
            if bg_dict:
                bg_1 = var_x_f(**get_var(bg_dict, "_sideband"))
                bg_2 = var_y_f(**get_var(bg_dict, "_sideband"))
                bg_weights = bg_dict["sideband_weights"]
                plt.hist2d(
                    bg_1,
                    bg_2,
                    bins=[x_bins, y_bins],
                    weights=bg_weights,
                    range=[x_range, y_range],
                    cmin=1e-12,
                )
                plot_axis()
                plt.title(title, fontsize="xx-large")
                plt.colorbar()
                plt.savefig(prefix + k + "_bkg_hist")
                plt.clf()
                print("Finish plotting 2D sideband histogram " + prefix + k)
            else:
                print("There's no bkg input")
        ## fit pdf
        if "fitted" in plot_figs:
            phsp_weights = phsp_dict["MC_total_fit"]
            plt.hist2d(
                phsp_1,
                phsp_2,
                bins=[x_bins, y_bins],
                weights=phsp_weights,
                range=[x_range, y_range],
                cmin=1e-12,
            )
            plot_axis()
            plt.title(title, fontsize="xx-large")
            plt.colorbar()
            plt.savefig(prefix + k + "_fitted")
            plt.clf()
            print("Finish plotting 2D fitted " + prefix + k)
        if "pull" in plot_figs:
            n = max(int(np.log(data_1.shape[0] / 50) / np.log(4)), 2)
            pull_binning = v.get("adaptive_binning", [[2, 2]] * n)
            pull_scatter_style = v.get(
                "pull_scatter_style", {"c": "black", "s": 1}
            )
            pull_cmap = v.get("pull_cmap", "jet")
            plot_function_2dpull(
                data_dict,
                phsp_dict,
                bg_dict,
                var1=v["x"],
                var2=v["y"],
                where=where,
                binning=pull_binning,
                scatter_style=pull_scatter_style,
            )
            plot_axis()
            plt.savefig(prefix + k + "_pull")
            plt.clf()
            print("Finish plotting 2D pull " + prefix + k)


@ConfigLoader.register_function()
def get_dalitz(config, a, b):
    decay = config.get_decay(False)
    da = decay.get_decay_chain(a)
    db = decay.get_decay_chain(b)
    pa = decay.get_particle(a)
    pb = decay.get_particle(b)

    for i in da:
        if pa in i.outs:
            topa = i.core
        if pa == i.core:
            outs_a = i.outs
    for i in db:
        if pb in i.outs:
            topb = i.core
        if pb == i.core:
            outs_b = i.outs
    same_finals = [i for i in outs_a if i in outs_b]
    p1 = [i for i in outs_a if i not in same_finals]
    p3 = [i for i in outs_b if i not in same_finals]
    check = topa == topb
    check = check and len(same_finals) == 1
    check = check and len(p1) == 1
    check = check and len(p3) == 1
    if not check:
        return None
    p0, p1, p2, p3 = topa, p1[0], same_finals[0], p3[0]
    p0, p1, p2, p3 = [
        config.get_decay().get_particle(str(i)) for i in [p0, p1, p2, p3]
    ]
    m0, m1, m2, m3 = map(lambda x: x.get_mass(), [p0, p1, p2, p3])
    return m0, m1, m2, m3


@ConfigLoader.register_function()
def get_dalitz_boundary(config, a, b, N=1000):
    dalitz = get_dalitz(config, a, b)
    assert dalitz is not None, "not valid daliz plot"
    m0, m1, m2, m3 = dalitz
    # print(m0, m1, m2, m3)
    from tf_pwa.angle import kine_min_max

    s12_min, s12_max = float(m1 + m2), float(m0 - m3)
    s12 = np.linspace(s12_min**2, s12_max**2, N)
    s23_min, s23_max = kine_min_max(s12, *map(float, [m0, m1, m2, m3]))
    return s12, np.stack([s23_min, s23_max], axis=-1)


def plot_function_2dpull(
    data_dict,
    phsp_dict,
    bg_dict,
    var1="x",
    var2="y",
    binning=[[2, 2]] * 3,
    where={},
    ax=plt,
    cut_zero=True,
    plot_scatter=True,
    scatter_style={"s": 1, "c": "black"},
    cmap="jet",
    **kwargs
):
    import matplotlib as mpl
    import matplotlib.colors as mcolors
    import matplotlib.patches as mpathes

    from tf_pwa.adaptive_bins import AdaptiveBound

    if cut_zero:
        cut = data_dict["data_weights"] != 0
    else:
        cut = np.ones(data_dict["data_weights"].shape, dtype=np.bool)
    (var_x_f, var_y_f), get_var = build_read_var_function(
        [var1, var2], where=where
    )
    x = var_x_f(**get_var(data_dict, ""))[cut]
    y = var_y_f(**get_var(data_dict, ""))[cut]
    w = data_dict["data_weights"][cut]
    x_phsp = var_x_f(**get_var(phsp_dict, "_MC"))
    y_phsp = var_y_f(**get_var(phsp_dict, "_MC"))
    w_phsp = phsp_dict["MC_total_fit"]
    data_cut = np.array([x, y])
    phsp_cut = np.array([x_phsp, y_phsp])
    base_bound = (
        np.min(phsp_cut, axis=-1) - 1e-6,
        np.max(phsp_cut, axis=-1) + 1e-6,
    )
    adapter = AdaptiveBound(data_cut, binning, base_bound)
    phsps = adapter.split_data(np.array([x_phsp, y_phsp, w_phsp]))
    datas = adapter.split_data(np.array([x, y, w]))
    if bg_dict != {}:
        x_bg = var_x_f(**get_var(bg_dict, "_sideband"))
        y_bg = var_y_f(**get_var(bg_dict, "_sideband"))
        w_bg = bg_dict["sideband_weights"]
        bgs = adapter.split_data(np.array([x_bg, y_bg, w_bg]))
    bound = adapter.get_bounds()
    numbers = []
    pulls = []
    int_norm = 1
    for i, bnd in enumerate(bound):
        min_x, min_y = bnd[0]
        max_x, max_y = bnd[1]
        ndata = np.sum(datas[i][2])
        nmc = np.sum(phsps[i][2])
        if bg_dict != {}:
            nmc += np.sum(bgs[i][2])
        numbers.append((ndata, nmc))
        pulls.append((ndata - nmc) / np.sqrt(nmc))

    max_weight = max(np.max(np.abs(pulls)), 5)

    my_cmap = plt.get_cmap(cmap)
    if ax == plt:
        ax = plt.gca()  # fig, ax = plt.subplots()
    if plot_scatter:
        ax.scatter(x, y, **scatter_style)
    for i, bnd in enumerate(bound):
        min_x, min_y = bnd[0]
        max_x, max_y = bnd[1]
        # print(weights[i]) # max_weight)
        rect = mpathes.Rectangle(
            (min_x, min_y),
            max_x - min_x,
            max_y - min_y,
            linewidth=1,
            facecolor=my_cmap(pulls[i] / max_weight / 2 + 0.5),  # max_weight),
            edgecolor="none",  # black",
            zorder=-1,
        )  # cmap(weights[i]/max_weight))
        ax.add_patch(rect)

    normal = mpl.colors.Normalize(vmin=-max_weight, vmax=max_weight)
    im = mpl.cm.ScalarMappable(norm=normal, cmap=my_cmap)
    # ax.colorbar(im)
    ax.get_figure().colorbar(im, ax=ax)
    ax.set_title(
        "$\\chi^2/Nbins={:.2f}/{}$".format(
            np.sum(np.abs(pulls) ** 2), len(bound)
        )
    )
    ax.set_xlim([np.min(x_phsp), np.max(x_phsp)])
    ax.set_ylim([np.min(y_phsp), np.max(y_phsp)])
    ax.set_xlabel(var1)
    ax.set_ylabel(var2)


@ConfigLoader.register_function()
def plot_adaptive_2dpull(
    config,
    var1,
    var2,
    binning=[[2, 2]] * 3,
    ax=plt,
    where={},
    cut_zero=True,
    plot_scatter=True,
    scatter_style={"s": 1, "c": "black"},
    **kwargs
):
    pull_kwargs = {
        "var1": var1,
        "var2": var2,
        "binning": binning,
        "where": where,
        "plot_scatter": plot_scatter,
        "scatter_style": scatter_style,
        "cut_zero": cut_zero,
    }

    def my_plot_function_2dpull(*args, **kwargs):
        plot_function_2dpull(*args, **pull_kwargs, **kwargs)

    config.plot_partial_wave(
        plot_function=my_plot_function_2dpull, combine_plot=True, **kwargs
    )


def hist_error(data, bins=50, xrange=None, weights=1.0, kind="poisson"):
    if not hasattr(weights, "__len__"):
        weights = [weights] * data.__len__()
    data_hist = np.histogram(data, bins=bins, weights=weights, range=xrange)
    # ax.hist(fd(data[idx].numpy())components,range=xrange,bins=bins,histtype="step",label="data",zorder=99,color="black")
    data_y, data_x = data_hist[0:2]
    data_x = (data_x[:-1] + data_x[1:]) / 2
    if kind == "poisson":
        data_err = np.sqrt(
            np.abs(data_y)
        )  # data_err = np.maximum(np.sqrt(np.abs(data_y)),1)
    elif kind == "binomial":
        n = data.shape[0]
        p = data_y / n
        data_err = np.sqrt(p * (1 - p) * n)
    else:
        raise ValueError("unknown error kind {}".format(kind))
    return data_x, data_y, data_err


def hist_line(
    data, weights, bins, xrange=None, inter=1, kind="UnivariateSpline"
):
    """interpolate data from hostgram into a line

    >>> import numpy as np
    >>> import matplotlib.pyplot
    >>> z = np.random.normal(size=1000)
    >>> x, y = hist_line(z, None, 50)
    >>> a = plt.plot(x, y)

    """
    y, x = np.histogram(data, bins=bins, range=xrange, weights=weights)
    num = data.shape[0] * inter
    return interp_hist(x, y, num=num, kind=kind)


def hist_line_step(
    data, weights, bins, xrange=None, inter=1, kind="quadratic"
):
    """

    >>> import numpy as np
    >>> import matplotlib.pyplot
    >>> z = np.random.normal(size=1000)
    >>> x, y = hist_line_step(z, None, 50)
    >>> a = plt.step(x, y)

    """
    y, x = np.histogram(data, bins=bins, range=xrange, weights=weights)
    dx = x[1] - x[0]
    x = (x[:-1] + x[1:]) / 2
    x = np.concatenate([[x[0] - dx], x, [x[-1] + dx]])
    y = np.concatenate([[0], y, [0]])
    return x, y


def export_legend(ax, filename="legend.pdf", ncol=1):
    """
    export legend in Axis `ax` to file `filename`
    """
    fig2 = plt.figure()
    ax2 = fig2.add_subplot()
    ax2.axis("off")
    legend = ax2.legend(
        *ax.get_legend_handles_labels(), frameon=False, loc="lower center"
    )
    fig = legend.figure
    fig.canvas.draw()
    bbox = legend.get_window_extent().transformed(
        fig.dpi_scale_trans.inverted()
    )
    fig.savefig(filename, dpi="figure", bbox_inches=bbox)
    plt.close(fig2)
    plt.close(fig)
