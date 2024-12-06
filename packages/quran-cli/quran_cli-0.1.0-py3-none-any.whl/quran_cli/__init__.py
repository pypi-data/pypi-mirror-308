""" Quran CLI, A tool to generate the most sophisticated Quran data. """

import json
from pathlib import Path
import sqlite3
from typing import List, Literal, Tuple


def execute_sql_script(db_name: str, script: str) -> None:
    """
    Executes a SQL script.

    Args:
        db_name (str): Database filename
        script (str): SQL script string
    """

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.executescript(script)
    connection.commit()
    connection.close()


def execute_sql_file(db_name: str, path: Path) -> None:
    """
    Executes a SQL file.

    Args:
        db_name (str): Database filename
        file (str): SQL script filename
    """

    with open(path, "r", encoding="utf-8") as file:
        execute_sql_script(db_name, file.read())


def create_db(db_name: str) -> None:
    """
    Creates the database to insert quran text.

    Args:
        name (str): Database filename
    """

    execute_sql_file(
        db_name,
        Path(__file__).parent / "assets" / "schemas" / "initial.sql",
    )


def insert_initial_data(db_name: str) -> None:
    """
    Inserts the Quran text into the database

    Args:
        db_name (str): Database filename
    """

    execute_sql_file(
        db_name,
        Path(__file__).parent / "assets" / "data" / "initial.sql",
    )


def apply_normalized_schema(db_name: str) -> None:
    """
    Creates the tables to normalize the initial db.

    Args:
        db_name (str): Database filename
    """

    execute_sql_file(
        db_name,
        Path(__file__).parent / "assets" / "schemas" / "normalized.sql",
    )


def insert_chapters(db_name: str) -> None:
    """
    Insert chapters (Al-Suwar) data into the database.

    Args:
        db_name (str): Database filename
    """

    execute_sql_file(
        db_name,
        Path(__file__).parent / "assets" / "data" / "chapters.sql",
    )


def get_verse(
    db_name: str,
    chapter_id: int,
    verse_number: int,
) -> Tuple[int, int, int, str]:
    """
    Get a verse from the database.

    Args:
        db_name (str): Database filename
        chapter_id (int): Chapter ID
        verse_number (int): Verse number

    Returns:
        Tuple[int, int, int, str]: Tuple with the verse data
    """

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM quran WHERE chapter_id = ? AND number = ?",
        (chapter_id, verse_number),
    )
    verse = cursor.fetchone()
    connection.close()

    return verse


def extract_range_data(
    db_name: str,
    start: Tuple[int, int],
    end: Tuple[int, int],
) -> Tuple[int, int]:
    """
    Extracts the verse range from the database as (start_verse_id, end_verse_id).

    Args:
        db_name (str): Database filename
        start (Tuple[int, int]): Start chapter_id and verse_number
        end (Tuple[int, int]): End chapter_id and verse_number

    Returns:
        Tuple[int, int]: Tuple with the start and end verse ids
    """

    start_verse = get_verse(db_name, start[0], start[1])
    end_verse = get_verse(db_name, end[0], end[1])

    return (start_verse[0], end_verse[0] - 1)


def get_range_data(
    db_name: str,
    key: Literal["parts", "pages", "quarters"],
) -> List[Tuple[int, int]]:
    """
    Extracts the verse range from the database as (start_verse_id, end_verse_id).

    Args:
        db_name (str): Database filename

    Returns:
        Tuple[int, int]: Tuple with range data
    """

    with open(
        Path(__file__).parent / "assets" / "data" / "metadata.json",
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)[key]

        res = []
        for index, item in enumerate(data):
            if index < len(data) - 1:
                res.append(extract_range_data(db_name, item, data[index + 1]))
            else:
                res.append((res[-1][1] + 1, 6236))

        return res


def insert_verses(db_name: str) -> None:
    """
    Insert verses (Al-Aayat) data into the database.

    Args:
        db_name (str): Database filename
    """

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    verses = cursor.execute(
        'SELECT "number", "content", "chapter_id" FROM "quran"'
    ).fetchall()

    for verse in verses:
        cursor.execute(
            'INSERT INTO "verses" ("number", "content", "chapter_id") VALUES (?, ?, ?);',
            verse,
        )

    connection.commit()
    connection.close()


def insert_metadata(db_name: str) -> None:
    """
    Insert parts, pages metadata into the database.

    Args:
        db_name (str): Database filename

    Returns:
        bool: True if the data is inserted successfully else False.
    """

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    for i in range(1, 31):
        cursor.execute("INSERT INTO parts (name) VALUES (?)", (f"Part {i}",))

    for i in range(1, 61):
        cursor.execute("INSERT INTO groups (name) VALUES (?)", (f"Group {i}",))

    for i in range(1, 241):
        cursor.execute("INSERT INTO quarters (name) VALUES (?)", (f"Quarter {i}",))

    for i in range(1, 605):
        cursor.execute("INSERT INTO pages (name) VALUES (?)", (f"Page {i}",))

    connection.commit()
    connection.close()


def add_verse_related_fields(db_name: str) -> None:
    """
    Add part_id, group_id, quarter_id and page_id to verses table.

    Args:
        db_name (str): Database filename
    """

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    key_cols = [
        ("parts", "part_id"),
        ("pages", "page_id"),
        ("quarters", "quarter_id"),
    ]
    for key, col in key_cols:
        data = get_range_data(db_name, key)

        for i, item in enumerate(data, start=1):
            cursor.execute(
                f'UPDATE "verses" SET {col} = ? where "id" between ? AND ?',
                (i, *item),
            )

        connection.commit()

    # Insert group data
    data = get_range_data(db_name, "quarters")
    ahzab = [
        (data[i][0], data[i + 3][1] if i + 4 < len(data) - 1 else 6236)
        for i in range(0, 240, 4)
    ]

    for i, item in enumerate(ahzab, start=1):
        cursor.execute(
            'UPDATE "verses" SET group_id = ? where "id" between ? AND ?',
            (i, *item),
        )

    connection.commit()
    connection.close()


def add_verse_count(db_name: str) -> None:
    """
    Add verse_count to tables.

    Args:
        db_name (str): Database filename
    """

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    tables = ["groups", "parts", "quarters", "pages"]
    for table in tables:
        data = cursor.execute(
            f'SELECT COUNT(*) FROM "verses" GROUP BY "{table[0:-1]}_id"'
        ).fetchall()

        for i, item in enumerate(data, start=1):
            cursor.execute(
                f'UPDATE {table} SET "verse_count" = ? WHERE "id" = ?', (item[0], i)
            )

    connection.commit()
    connection.close()


def add_related_fields(db_name: str) -> None:
    """
    Add chapter_id, part_id, group_id and quarter_id to pages, groups and quartes tables.

    Args:
        db_name (str): Database filename
    """

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    data = cursor.execute(
        'SELECT "chapter_id", "part_id", "group_id", "quarter_id" FROM "verses" GROUP BY "page_id"'
    ).fetchall()

    for item in enumerate(data, start=1):
        cursor.execute(
            'UPDATE "pages" SET "chapter_id" = ?, "part_id" = ?, "group_id" = ?, "quarter_id" = ? WHERE "id" = ?',
            (*item[1], item[0]),
        )

    data = cursor.execute(
        'SELECT "part_id" FROM "verses" GROUP BY "group_id"'
    ).fetchall()

    for item in enumerate(data, start=1):
        cursor.execute(
            'UPDATE "groups" SET "part_id" = ? WHERE "id" = ?',
            (*item[1], item[0]),
        )

    data = cursor.execute(
        'SELECT "part_id", "group_id" FROM "verses" GROUP BY "quarter_id"'
    ).fetchall()

    for item in enumerate(data, start=1):
        cursor.execute(
            'UPDATE "quarters" SET "part_id" = ?, "group_id" = ? WHERE "id" = ?',
            (*item[1], item[0]),
        )

    connection.commit()
    connection.close()
