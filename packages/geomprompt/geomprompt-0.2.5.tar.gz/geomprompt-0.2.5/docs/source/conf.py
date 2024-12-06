"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html

This file is based on the GDA-Cookiecutter, version 2.1.9
In most cases, it should not need to be edited by hand.  See
https://gitlab.geomdata.com/geomdata/gda-cookiecutter/-/blob/master/README.md
for instructions on how to update to a newer version of the GDA-Cookiecutter.
"""

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import pathlib
import sphinx_rtd_theme
import sys
import toml

sys.path.insert(0, os.path.abspath("../../"))


# -- Project information -----------------------------------------------------

project = "GeomPrompt"
copyright = "Copyright (c) 2024, Geometric Data Analytics, Inc"
author = "Kenneth R. Ball"


# The full version, including alpha/beta/rc tags
pyproject_path = pathlib.Path("../../pyproject.toml")
release = toml.load(pyproject_path.open())["project"]["version"]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["nbsphinx", "sphinx_rtd_theme", "sphinx.ext.autodoc"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]

nbsphinx_kernel_name = "geomprompt"

html_favicon = "_static/favicon.ico"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme_options = {
    "navigation_depth": 3,
    "logo_only": True,
}

html_logo = "_static/logo.png"

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y"
