# Save Text File

save_text_file provides a function to save a string, with optional overwrite check and traling newline support.

## Usage
```python
from pfmsoft.eve_snippets import save_text_file
from pathlib import Path

output_dir = Path("/tmp/examples")
slug = "computed_value"

# Default values for the function:
# overwrite: bool = False,
# encoding: str = "utf-8",
# add_newline: bool = True,

output_filepath = save_text_file(
    text="A string to save to a file",
    directory=output_dir,
    filename=f"saved_file{slug}",
)
```