# Create-fastapi-cli

A powerful CLI tool for quickly creating FastAPI projects, **support >=Python 3.10**.

## Table of Contents
- [Create-fastapi-cli](#create-fastapi-cli)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Usage](#usage)
      - [Run](#run)
      - [Lint](#lint)
      - [Format](#format)
      - [Type check](#type-check)
      - [Test](#test)
  - [Project Structure](#project-structure)
  - [Development](#development)
  - [Testing](#testing)
  - [Publish](#publish)
  - [Support](#support)

## Features
- Quick project setup with best practices
- Support for both pip and poetry dependency management
- Customizable project templates
- Built-in testing and linting tools

## Installation

```shell
pip install create-fastapi-cli
```

## Quick Start
Create a new FastAPI project in seconds:

```shell
# poetry recommended
create-fastapi-cli --name myapp --install --poetry
# pip
create-fastapi-cli --name myapp --install
```

| Option      | Description                                                                     |
| ----------- | ------------------------------------------------------------------------------- |
| `--name`    | The name of the project.                                                        |
| `--install` | Install dependencies.                                                           |
| `--poetry`  | Use poetry to manage project, if not specified, will use pip to manage project. |
| `--version` | The version of the cli.                                                         |

## Usage

#### Run

Start the FastAPI server:

```shell
cd myapp

# pip
uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level=info --reload

# poetry
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level=info --reload
```

#### Lint

```shell
ruff check --fix
```

#### Format

```shell
ruff format
```

#### Type check

```shell
pytype
```

#### Test

```shell
pytest
```

## Project Structure

```
myapp
├── confs
│   ├── config.yaml
│   └── unit-test.yaml
├── Dockerfile
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
├── src
│   ├── config.py
│   ├── constants.py
│   ├── database.py
│   ├── decos.py
│   ├── __init__.py
│   ├── main.py
│   ├── routers
│   │   ├── base.py
│   │   ├── greeting
│   │   │   ├── __init__.py
│   │   │   └── router.py
|   |   |   └── schemas.py
│   │   ├── __init__.py
│   └── utils.py
└── tests
    ├── conftest.py
    ├── __int__.py
    └── test_greeting.py
```

## Development

Update the template code and test it locally. **You need to test service and run test before publish.**

```shell
pip install -e .

# pip
create-fastapi-cli --name myapp --install

# poetry
create-fastapi-cli --name myapp --install --poetry
```

## Testing

Test will create two projects(>=Python 3.10), one is with Poetry, another is with Pip.

## Publish

```shell
poetry publish --repository deeproute -u <username> -p <password>
```

## Support

If you have any questions or need support, please contact us at `yugang.cao12@gmail.com`.
