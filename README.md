# Wiz

Hacker-vibe command-line shortcut manager. Store frequently used commands as
named shortcuts and run them instantly from any terminal.

Status: pre-alpha. The CLI is in early scaffolding.

## Table of Contents

- Install
- Usage
- CLI Contract
- Config
- Roadmap
- Contributing
- License

## Install

Not packaged yet. Run from source:

```text
python main/main.py help
```

## Usage

Current behavior includes `help`, `list`, and `add`.

```text
python main/main.py help
python main/main.py list
python main/main.py add build "python -m pytest -q"
```

## CLI Contract

Planned interface (draft):

- `wiz add <name> <command>`
- `wiz delete <name>`
- `wiz run <name>`
- `wiz list`
- `wiz help`
- `wiz export`

Example usage:

```text
wiz add build "python -m pytest -q"
wiz add serve "python -m http.server 8000"
wiz list
wiz run build
```

## Config

Stored at `main/config.json` (next to `main.py`). Format is JSON:

```json
{
  "build": "python -m pytest -q",
  "serve": "python -m http.server 8000"
}
```

## Roadmap

- MVP CLI (add, delete, run, list)
- Export to shell aliases
- Search and tags
- Usage stats

## Contributing

See `CONTRIBUTING.md`.

## License

MIT. See `LICENSE`.
