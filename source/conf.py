# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "CADCAST Estimation Plugin for Cura Documentation"
copyright = "2026, CStoner"
author = "CStoner"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_togglebutton"
    ]

myst_enable_extensions = [
    "attrs_block",
    "colon_fence",
    "attrs_inline",
    "deflist"
]

html_static_path = ['explanation/_static']

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 2
}
html_static_path = ["_static"]
