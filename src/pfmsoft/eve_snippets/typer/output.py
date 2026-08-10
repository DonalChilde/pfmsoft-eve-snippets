"""A module for outputting data to stdout or a file."""

from pathlib import Path

from rich.console import Console

from pfmsoft.eve_snippets.files.save_text_file import save_text_file


def output_to_stdout_or_file(
    data_string: str,
    filepath: Path,
    overwrite: bool,
    messenger: Console,
) -> None:
    """Outputs the data to a file or stdout.

    Args:
        data_string: The string data to output.
        filepath: The path to the output file. If the filepath is Path("-"), output to stdout.
        overwrite: Whether to overwrite the file if it exists.
        messenger: The Console object for printing messages.

    Raises:
        FileExistsError: If the file already exists and overwrite is False.
    """
    if filepath == Path("-"):
        print(data_string)
    else:
        try:
            output_path = save_text_file(
                text=data_string,
                directory=filepath.parent,
                filename=filepath.name,
                overwrite=overwrite,
            )
        except FileExistsError as e:
            messenger.print(
                f"File {filepath} already exists. Use --overwrite to overwrite it."
            )
            raise e
        messenger.print(f"Output saved to {output_path}")
