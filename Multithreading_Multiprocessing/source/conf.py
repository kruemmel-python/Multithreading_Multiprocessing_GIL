# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../'))  # Dies fügt den Pfad zu deinen Modulen hinzu

# -- Project information -----------------------------------------------------
project = 'Multithreading Multiprocessing (GIL)'
copyright = '2024, Ralf Krümmel'
author = 'Ralf Krümmel'
release = '1'

# -- General configuration ---------------------------------------------------
extensions = [
    'recommonmark',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

autosummary_generate = True
templates_path = ['_templates']
exclude_patterns = []

language = 'de'

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']

# Modul- und Stichwortverzeichnisse aktivieren
html_domain_indices = True
html_use_index = True
