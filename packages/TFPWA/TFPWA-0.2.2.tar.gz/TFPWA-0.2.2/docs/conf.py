"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import shutil
import subprocess
import sys

this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, this_dir + "/..")

from tf_pwa.amp import DECAY_MODEL, PARTICLE_MODEL, base, get_config
from tf_pwa.experimental import (  # type: ignore  # pylint: disable=unused-import
    extra_amp,
)

# -- Project information -----------------------------------------------------
project = "TFPWA"
copyright = "2020, Yi Jiang"  # pylint: disable=redefined-builtin
author = "Yi Jiang"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_gallery.gen_gallery",
    "matplotlib.sphinxext.plot_directive",
]
exclude_patterns = [
    ".DS_Store",
    "Thumbs.db",
    "_build",
]
source_suffix = [
    ".rst",
]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_title = "TFPWA"
viewcode_follow_imported_members = True

# -- Options for API ---------------------------------------------------------
add_module_names = False
autodoc_mock_imports = [
    "iminuit",
    "tensorflow",
]

# Cross-referencing configuration
default_role = "py:obj"
primary_domain = "py"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Generate API skeleton ----------------------------------------------------
shutil.rmtree("api", ignore_errors=True)
subprocess.call(
    " ".join(
        [
            "sphinx-apidoc",
            "-o api/",
            "--force",
            "--no-toc",
            "--templatedir _templates",
            "--separate",
            "../tf_pwa/",
            # exclude patterns
            "../tf_pwa/tests",
            "../tf_pwa/config_loader/tests/*",
            "../tf_pwa/*/test_*",
        ]
    ),
    shell=True,
)


# -- Generate available resonance models --------------------------------------
def add_indent(s, number=2):
    ret = ""
    for i in s.split("\n"):
        ret += " " * number + i + "\n"
    return ret


def gen_particle_model():
    particle_model_doc = """
--------------------------
Available Resonances Model
--------------------------

"""
    models = []
    model_params = {}
    for idx, (k, v) in enumerate(get_config(PARTICLE_MODEL).items(), 1):
        doc_i = v.__doc__
        if v.__doc__ is None and v.get_amp.__doc__ is None:
            continue
        if v.__doc__ is None:
            doc_i = v.get_amp.__doc__

        if v not in models:
            models.append(v)
        if v in model_params:
            model_params[v]["name"].append(f'"{k}"')
        else:
            model_params[v] = {"name": [f'"{k}"'], "doc": doc_i}

    for idx, v in enumerate(models):
        name_list = model_params[v]["name"]
        name = ", ".join(name_list)
        doc_i = model_params[v]["doc"]
        particle_model_head = (
            f"\n{idx+1}. :code:`{name}`"
            f" (`~{v.__module__}.{v.__qualname__}`)\n"
        )
        particle_model_doc += particle_model_head
        particle_model_doc += "^" * (len(particle_model_head) - 2) + "\n\n"
        idx += 1
        particle_model_doc += add_indent(doc_i) + "\n\n"

    with open(
        os.path.dirname(os.path.abspath(__file__)) + "/particle_model.rst", "w"
    ) as f:
        f.write(particle_model_doc)


def gen_decay_model():
    decay_model_doc = """
--------------------------
Available Decay Model
--------------------------

"""
    all_models = {}
    model_params = {}
    for idx, ((n, k), v) in enumerate(get_config(DECAY_MODEL).items(), 1):
        doc_i = v.__doc__
        if v.__doc__ is None and v.get_amp.__doc__ is None:
            continue
        if v.__doc__ is None:
            doc_i = v.get_amp.__doc__

        if n not in all_models:
            all_models[n] = []
        if v not in all_models[n]:
            all_models[n].append(v)
        if v in model_params:
            model_params[v]["name"].append(f'"{k}"')
        else:
            model_params[v] = {"name": [f'"{k}"'], "doc": doc_i}

    for n, models in all_models.items():
        decay_model_doc += """
{}-body decays
----------------
""".format(
            n
        )
        for idx, v in enumerate(models):
            name_list = model_params[v]["name"]
            name = ", ".join(name_list)
            doc_i = model_params[v]["doc"]
            decay_model_head = (
                f"\n{idx+1}. :code:`{name}`"
                f" (`~{v.__module__}.{v.__qualname__}`)\n"
            )
            decay_model_doc += decay_model_head
            decay_model_doc += "^" * (len(decay_model_head) - 2) + "\n\n"
            idx += 1
            decay_model_doc += add_indent(doc_i) + "\n\n"

    with open(
        os.path.dirname(os.path.abspath(__file__)) + "/decay_model.rst", "w"
    ) as f:
        f.write(decay_model_doc)


gen_particle_model()
gen_decay_model()


sphinx_gallery_conf = {
    "examples_dirs": "../examples",  # path to your example scripts
    "gallery_dirs": "auto_examples",  # path to where to save gallery generated output
    "line_numbers": True,
    "run_stale_examples": True,
    "filename_pattern": "ex",
}
