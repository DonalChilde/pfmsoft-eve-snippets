__project_namespace__ = "pfmsoft"
__author__ = "Chad Lowe"
__email__ = "pfmsoft.dev@gmail.com"
__app_name__ = "eve-snippets"
#######################################################################################
# Update in pyproject.toml, as uv build backend does not yet support dynamic metadata #
# https://github.com/astral-sh/uv/issues/11718                                        #
#######################################################################################
__description__ = "A command line first interface to the Eve Online API"
__version__ = "0.1.0"
__release__ = __version__
#######################################################################################
__url__ = "https://github.com/DonalChilde/pfmsoft-eve-snippets"
__license__ = "MIT"

from pfmsoft.eve_snippets.files.save_text_file import save_text_file
from pfmsoft.eve_snippets.markdown import markdown_table
from pfmsoft.eve_snippets.pydantic import json_io

__all__ = ["json_io", "markdown_table", "save_text_file"]
