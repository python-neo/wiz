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
pip install -r requirements.txt
python -m main.main help
```

## Usage

Current behavior includes `help`, `list`, `add`, `delete`, `replace`, `run`, and `export`.

```text
python -m main.main help
python -m main.main list
python -m main.main add build "python -m pytest -q"
python -m main.main run build
python -m main.main export
python -m main.main delete build
python -m main.main replace build "python -m pytest"
python -m main.main --no-color list
python -m main.main --version
```

## Flags

- `--version` prints the Wiz version and exits
- `--no-color` disables colored output

Note: flags must appear before the command.

## CLI Contract

Supported commands:

- `wiz add <name> <command>`
- `wiz delete <name>`
- `wiz run <name>`
- `wiz list`
- `wiz help`
- `wiz export`
- `wiz replace <name> <command>`

Example usage:

```text
wiz add build "python -m pytest -q"
wiz add serve "python -m http.server 8000"
wiz list
wiz run build
wiz export
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
