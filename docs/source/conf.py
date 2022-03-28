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
import os
import sys
from configparser import ConfigParser, ExtendedInterpolation
import sphinx_rtd_theme

autoapi_type = 'python'
autoapi_dirs = ['../../pycodeanalyzer']
autoapi_generate_api_docs = False

import autoapi
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------

project = 'pycodeanalyzer'
copyright = '2022, Giovanni Mion'
author = 'Giovanni Mion'

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("../../.bumpversion.cfg")

version = config["bumpversion"]["current_version"]
# The full version, including alpha/beta/rc tags.
release = version

todo_include_todos = True


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.githubpages',
    'sphinx.ext.viewcode',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
    'autoapi.extension',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
    'vcs_pageview_mode': 'blob',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': -1,
    'includehidden': False,
    'titles_only': False,
}

intersphinx_mapping = {
    "Python": ('https://docs.python.org/3.7/', None),
    "robotpy-cppheaderparser": ('https://cppheaderparser.readthedocs.io/en/stable/',None),
    "Flask" : ('https://flask.palletsprojects.com/en/latest/', None),
    "Flask-SocketIO" : ('https://flask-socketio.readthedocs.io/en/latest/', None),
    "Flask-Classful" : ('https://flask-classful.teracy.org/',None),
    "simple-websocket" : ('https://simple-websocket.readthedocs.io/en/latest/',None),
    "injector" : ('https://injector.readthedocs.io/en/latest/',None),
    "pathlib" : ('https://pathlib.readthedocs.io/en/latest/',None),
    "astroid" : ('https://pylint.pycqa.org/projects/astroid/en/latest/',None),
    "simplejson" : ('https://simplejson.readthedocs.io/en/latest/',None),
    "jsonpickle" : ('https://jsonpickle.readthedocs.io/en/latest/',None),
}
