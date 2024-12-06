""" Interact with Quran db using SQL """

from pathlib import Path
import sqlite3
from typing import Annotated
import typer
from rich import box, print
from rich.console import Console
from rich.table import Table


def explore(
    database: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, help="Database name"),
    ]
) -> None:
    """
    Explore the Quran database with SQL.

    Args:
        database (Path): Database file.

    Examples:

    ```bash
    # Create initial database
    quran-cli init db.sqlite3

    quran-cli explore db.sqlite3
    ```
    """

    db_name = (
        database.name
        if database.name.endswith((".sqlite3", ".db"))
        else database.name + ".sqlite3"
    )

    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        print(
            "[bold]SQLite 3 shell[/bold]\n"
            "Type [bold red]exit[/bold red] or [bold red]quit[/bold red] to exit."
        )

        while True:
            query = typer.prompt("SQLite3", prompt_suffix=" >>> ")

            if query.lower() in ("exit", "quit"):
                break

            results = cursor.execute(query).fetchall()

            console = Console()
            table = Table(
                title="Query Results",
                title_justify="left",
                title_style="bold",
                box=box.ROUNDED,
            )

            for column in cursor.description:
                table.add_column(column[0])

            for row in results:
                table.add_row(*[str(item) for item in row])

            console.print(table)

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
