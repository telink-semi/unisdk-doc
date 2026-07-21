"""
UniSDK Sphinx configuration (standalone version).

This file configures Sphinx to build the UniSDK developer documentation
for the standalone unisdk-doc repository. It uses sphinx_book_theme,
myst-parser for Markdown compatibility, and Breathe+Doxygen for API
reference generation from C header files (pulled from the main SDK
repo during CI builds).
"""

import os
import sys

# -- Path setup --------------------------------------------------------------
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -- Language / Version context (set via -D on CLI during CI) -----------------
# Default to English; CI passes -D language=zh for Chinese builds.
language = os.environ.get('UNISDK_DOC_LANG', 'en')

# Version from environment (set during CI builds), defaults to 'main'
_version = os.environ.get('UNISDK_DOC_VERSION', 'main')
_release = os.environ.get('UNISDK_DOC_RELEASE', _version)

# -- Project information -----------------------------------------------------

project = 'UniSDK'
copyright = 'Telink Semiconductor'
author = 'Telink Semiconductor'

# The full version, including alpha/beta/rc tags
release = _release
version = _version

# -- General configuration ---------------------------------------------------

extensions = [
    # Built-in extensions
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.intersphinx',
    'sphinx.ext.extlinks',
    'sphinx.ext.viewcode',

    # Internationalization (locale dir exists for translations)
    'sphinx_intl',

    # Markdown support via MyST
    'myst_parser',

    # Doxygen integration via Breathe
    'breathe',

    # UI enhancements
    'sphinx_copybutton',
    'sphinx_design',
    'sphinxcontrib.mermaid',

    # API navigation auto-discovery
    'sphinx.ext.autosummary',
]

# -- Internationalization -----------------------------------------------------
locale_dirs = [os.path.join(_BASE_DIR, 'locale')]
gettext_compact = False

# Source file suffixes: support both RST and MD
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The master toctree document (relative to source directory)
master_doc = 'index'

# Files/directories to exclude from processing
exclude_patterns = [
    '_build/**',
    '_doxygen/**',
    '_doxyfile_*',
    'doxygen.log',
    'Thumbs.db',
    '.DS_Store',
    'README.md',
]

# Suppress known warnings
suppress_warnings = [
    'myst.header',
    'myst.xref_missing',
    'misc.highlighting_failure',
    'ref.duplicate',
    'toc.not_included',
    'docutils',
    # Breathe C parser warnings for enum return types (e.g. "enum tlk_i2c_status")
    # and anonymous enums. These are non-fatal — affected functions still render
    # in the HTML, just without a fully parsed declaration signature.
    'breathe',
]

# The name of the Pygments (syntax highlighting) style to use
pygments_style = 'sphinx'

# -- MyST (Markdown) configuration -------------------------------------------

myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'tasklist',
    'attrs_inline',
    'attrs_block',
    'html_image',
]
myst_heading_anchors = 3

# -- Breathe (Doxygen) configuration -----------------------------------------

# During CI builds, the SDK source is checked out to ../_sdk_src/
# and Doxygen XML is generated there and copied/linked to _doxygen/
# If _doxygen doesn't exist (e.g. local builds without SDK headers),
# Breathe will gracefully skip API doc generation.
_doxygen_dir = os.path.join(os.path.dirname(__file__), '_doxygen')

if os.path.isdir(_doxygen_dir):
    breathe_projects = {
        'public_api': os.path.join(_doxygen_dir, 'public_api', 'xml'),
        'core_drivers': os.path.join(_doxygen_dir, 'core_drivers', 'xml'),
        'TL321X': os.path.join(_doxygen_dir, 'soc_TL321X', 'xml'),
        'TL721X': os.path.join(_doxygen_dir, 'soc_TL721X', 'xml'),
        'TLSR922X': os.path.join(_doxygen_dir, 'soc_TLSR922X', 'xml'),
        'TLSR952X': os.path.join(_doxygen_dir, 'soc_TLSR952X', 'xml'),
    }
    breathe_default_project = 'core_drivers'
else:
    # No Doxygen output available — Breathe will produce warnings
    # but Sphinx will still build the pure-documentation pages.
    breathe_projects = {}
    breathe_default_project = ''

breathe_domain_by_extension = {'h': 'c'}

# -- LaTeX (PDF) output configuration ----------------------------------------
# Used when building with xelatex (set via -D latex_engine=xelatex)
latex_elements = {
    'preamble': r'''
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
''',
}

# -- HTML theme configuration -------------------------------------------------

html_theme = 'sphinx_book_theme'
html_static_path = ['_static', 'stylesheets']
html_css_files = ['extra.css']

html_theme_options = {
    'repository_url': 'https://github.com/telink-semi/unisdk-doc',
    'use_repository_button': True,
    'use_edit_page_button': True,
    'use_issues_button': True,
    'home_page_in_toc': True,
    'toc_title': 'Contents',
    'show_navbar_depth': 2,
    'show_toc_level': 2,
    # Version info displayed in the footer
    'version': version,
    'version_selector': True,
}

# The name of an image file (relative to conf.py) to use as a favicon
html_favicon = '_static/favicon.svg'

# The name of an image file (relative to conf.py) to place at the top of
# the sidebar (sidebar logo)
html_logo = '_static/logo.svg'

# Pass version and language info to HTML templates
html_context = {
    'current_version': version,
    'current_language': language,
}

# -- Intersphinx configuration ------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Todo configuration -------------------------------------------------------

todo_include_todos = True
