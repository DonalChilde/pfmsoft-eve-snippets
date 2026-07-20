"""Eve Online API snippets for Python."""

from importlib.metadata import version

__project_namespace__ = "pfmsoft"
__author__ = "Chad Lowe"
__email__ = "pfmsoft.dev@gmail.com"
__app_name__ = "pfmsoft-eve-snippets"  # Must match project.name from pyproject.toml
__description__ = "Python code snippets for working with the Eve Online API."
__version__ = version(__app_name__)
__release__ = __version__
__url__ = "https://github.com/DonalChilde/pfmsoft-eve-snippets"
__license__ = "MIT"

from pfmsoft.eve_snippets.eve import eve_dates
from pfmsoft.eve_snippets.files.save_text_file import save_text_file
from pfmsoft.eve_snippets.httpx2 import http_session_factory
from pfmsoft.eve_snippets.markdown import markdown_table
from pfmsoft.eve_snippets.pydantic import json_io
from pfmsoft.eve_snippets.sqlite3 import connection_helpers
from pfmsoft.eve_snippets.yaml import yaml_io

__all__ = [
    "json_io",
    "markdown_table",
    "save_text_file",
    "yaml_io",
    "http_session_factory",
    "eve_dates",
    "connection_helpers",
]
