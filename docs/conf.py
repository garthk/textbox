"Sphinx configuration."  # noqa: INP001

from importlib import metadata

# We want an image in the README and include the README in the docs.
suppress_warnings = ["image.nonlocal_uri"]


# -- General configuration ----------------------------------------------------

extensions = [
    "myst_parser",
    "notfound.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_toolbox.more_autodoc.autoprotocol",
    "sphinx_toolbox.more_autodoc.typevars",
    "sphinxcontrib.mermaid",
]

myst_enable_extensions = [
    "colon_fence",
    "smartquotes",
    "deflist",
]
mermaid_init_js = "mermaid.initialize({startOnLoad:true,theme:'neutral'});"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "textbox"
tagline = "Remember text for you, wholesale."
author = "Garth Kidd"
copyright = f"2013, { author }"  # noqa: A001

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# The full version, including alpha/beta/rc tags.
release = metadata.version("textbox")
# The short X.Y version.
version = release.rsplit(".", 1)[0]

if "dev" in release:
    release = version = "UNRELEASED"

exclude_patterns = ["_build"]

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = "any"

nitpick_ignore = [
    ("py:class", "Context"),
    ("py:class", "EventDict"),
    ("py:class", "ILogObserver"),
    ("py:class", "PlainFileObserver"),
    ("py:class", "Processor"),
    ("py:class", "Styles"),
    ("py:class", "WrappedLogger"),
    ("py:class", "structlog.threadlocal.TLLogger"),
    ("py:class", "structlog.typing.EventDict"),
]

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# Move type hints into the description block, instead of the func definition.
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "furo"
html_theme_options = {}
html_logo = "_static/structlog_logo_small_transparent.png"
html_static_path = ["_static"]

htmlhelp_basename = "structlogdoc"

_logo = (
    "https://www.structlog.org/en/latest/_static/"
    "structlog_logo_small_transparent.png"
)
_descr = (
    "structlog makes logging in Python faster, less painful, and more "
    "powerful by adding structure to your log entries."
)
_title = f"{project}: {tagline.lower()}"
rst_epilog = f"""\
.. meta::
    :property=og:type: website
    :property=og:site_name: { _title }
    :property=og:description: { _descr }
    :property=og:author: { author }
    :property=og:image: { _logo }
"""

latex_documents = [
    ("index", "structlog.tex", "structlog Documentation", "Author", "manual"),
]

# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [("index", "structlog", "structlog Documentation", ["Author"], 1)]


# -- Options for Texinfo output -----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        "index",
        "structlog",
        "structlog Documentation",
        "Author",
        "structlog",
        "One line description of project.",
        "Miscellaneous",
    ),
]


# -- Options for Epub output --------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# GitHub has rate limits
linkcheck_ignore = [
    r"https://github.com/.*/(issues|pull|compare)/\d+",
    r"https://twitter.com/.*",
]

# Twisted's trac tends to be slow
linkcheck_timeout = 300

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
