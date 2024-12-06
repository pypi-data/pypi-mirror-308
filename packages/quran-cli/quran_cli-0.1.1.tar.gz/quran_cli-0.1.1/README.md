# Quran CLI

[![Continuous Integration](https://github.com/youzarsiph/quran-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/youzarsiph/quran-cli/actions/workflows/ci.yml)
[![Continuous Deployment](https://github.com/youzarsiph/quran-cli/actions/workflows/cd.yml/badge.svg)](https://github.com/youzarsiph/quran-cli/actions/workflows/cd.yml)
[![Black](https://github.com/youzarsiph/quran-cli/actions/workflows/black.yml/badge.svg)](https://github.com/youzarsiph/quran-cli/actions/workflows/black.yml)
[![Ruff](https://github.com/youzarsiph/quran-cli/actions/workflows/ruff.yml/badge.svg)](https://github.com/youzarsiph/quran-cli/actions/workflows/ruff.yml)

Quran CLI, A tool to generate the most sophisticated Quran data.

## Features

- User-friendly implementation
- Enhanced color and style options
- Integrated CI/CD capabilities
- Automated lint and format checks

## Getting Started

Install the package:

```bash
pip install quran-cli
```

**Usage**:

```console
quran-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `explore`: Explore the Quran database with SQL.
- `export`: Export Quran data to csv, json, xml format.
- `init`: Initialize Quran database.
- `normalize`: Normalize initial Quran database.

## `quran-cli explore`

Explore the Quran database with SQL.

Args:
    database (Path): Database file.

Examples:

```bash
# Create initial database
quran-cli init db.sqlite3

quran-cli explore db.sqlite3
```

**Usage**:

```console
quran-cli explore [OPTIONS] DATABASE
```

**Arguments**:

- `DATABASE`: Database name  [required]

**Options**:

- `--help`: Show this message and exit.

## `quran-cli export`

Export Quran data to csv, json, xml format.

Args:
    database (Path): Database filename.
    output (Path, optional): Output folder.
    format (str, optional): Export format.

Examples:

```bash
# Create initial database
quran-cli init db.sqlite3

# Normalize initial database
quran-cli normalize db.sqlite3

# Export normalized database
quran-cli export db.sqlite3 -f json
    ```

**Usage**:

```console
quran-cli export [OPTIONS] DATABASE
```

**Arguments**:

- `DATABASE`: Database name  [required]

**Options**:

- `-o, --output DIRECTORY`: Output folder  [default: quran]
- `-f, --format [csv|xml|json]`: Export format.  [default: json]
- `--help`: Show this message and exit.

## `quran-cli init`

Initialize Quran database.

Args:
    name (str): Database name.

Examples:

```bash
# Create initial database
quran-cli init db.sqlite3
```

**Usage**:

```console
quran-cli init [OPTIONS] DATABASE
```

**Arguments**:

- `DATABASE`: Database name  [required]

**Options**:

- `--help`: Show this message and exit.

## `quran-cli normalize`

Normalize initial Quran database.

Args:
    name (str): Database filename.

Examples:

```bash
# Create initial database
quran-cli init db.sqlite3

quran-cli normalize db.sqlite3
```

**Usage**:

```console
quran-cli normalize [OPTIONS] DATABASE
```

**Arguments**:

- `DATABASE`: Database name  [required]

**Options**:

- `--help`: Show this message and exit.

## License

This project is licensed under the MIT License.
