# {{ name }}

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Start:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level=info --reload
```

Lint:

```bash
ruff check --fix
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
