# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from opml import __version__

# -- Project information -----------------------------------------------------

project = 'PyOPML'
copyright = '2021, <a href="https://epoc.fr/">Epoc</a>'
author = '<a href="https://epoc.fr/">Epoc</a>'

# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

todo_include_todos = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

html_theme_options = {
    'show_powered_by': False,
    'github_button': False,
    'github_banner': True,
    'github_user': 'EpocDotFr',
    'github_repo': 'pyopml',
    'fixed_sidebar': True,
    'logo_name': True,
    'extra_nav_links': {
        'PyOPML @ GitHub': 'https://github.com/EpocDotFr/pyopml',
        'PyOPML @ PyPI': 'https://pypi.python.org/pypi/pyopml',
        'Issue Tracker': 'https://github.com/EpocDotFr/pyopml/issues',
        'Changelog': 'https://github.com/EpocDotFr/pyopml/releases',
    }
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

html_sidebars = { '**': ['about.html', 'navigation.html', 'searchbox.html'] }

html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.6', None),
}
