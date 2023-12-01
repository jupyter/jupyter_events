# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------
from __future__ import annotations

project = "jupyter_events"
copyright = "2019, Project Jupyter"
author = "Project Jupyter"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions: list = ["myst_parser", "jupyterlite_sphinx"]

try:
    import enchant  # noqa: F401

    extensions += ["sphinxcontrib.spelling"]
except ImportError:
    pass

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

source_suffix = [".rst", ".md"]


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "_contents",
    "Thumbs.db",
    ".DS_Store",
    "demo/demo-notebook.ipynb",
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_logo = "_static/jupyter_logo.png"

master_doc = "index"

# Configure jupyterlite to import jupyter_events package
jupyterlite_contents = ["demo/demo-notebook.ipynb"]

html_theme_options = {
    "logo": {
        "text": "Jupyter Events",
    },
    "navigation_with_keys": False,
    "icon_links": [
        {
            # Label for this link
            "name": "GitHub",
            # URL where the link will redirect
            "url": "https://github.com/jupyter/jupyter_events",  # required
            # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
            "icon": "fab fa-github-square",
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        },
        {
            "name": "jupyter.org",
            "url": "https://jupyter.org",
            "icon": "_static/jupyter_logo.png",
            "type": "local",
        },
    ],
}
