""" Init Quran db """

from pathlib import Path
from typing import Annotated
import typer
from rich import print

from quran_cli import create_db, insert_initial_data


def init(
    database: Annotated[Path, typer.Argument(dir_okay=False, help="Database name")]
) -> None:
    """
    Initialize Quran database.

    Args:
        name (str): Database name.

    Examples:

    ```bash
    # Create initial database
    quran-cli init db.sqlite3
    ```
    """

    db_name = (
        database.name
        if database.name.endswith((".sqlite3", ".db"))
        else database.name + ".sqlite3"
    )

    try:
        create_db(db_name)
        insert_initial_data(db_name)

        print("[bold green]Database created successfully[/bold green]")

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
