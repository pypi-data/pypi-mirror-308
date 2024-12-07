# {{ name }}

## Installation

```bash
poetry install
```

## Usage

Start:

```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level=info --reload
```

Lint:

```bash
ruff --fix
```

Format:

```bash
ruff format
```

Type check:

```bash
pytype
```

Test:

```bash
pytest
```
