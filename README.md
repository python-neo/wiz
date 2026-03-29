# Wiz

Hacker-vibe command-line shortcut manager. Store frequently used commands as
named shortcuts and run them instantly from any terminal.

Status: finished. The main CLI is now functional.

## Table of Contents

- Install
- Usage
- CLI Contract
- Config
- Roadmap
- Contributing
- License

## Install

Download the installer from the releases page, unzip, and run the `.exe`.
During setup, check the option to add Wiz to `PATH`.

After installation, open a new terminal and run:

```text
wiz help
```

## Releases

Latest release notes and downloads are published on GitLab:

- [Releases](https://gitlab.com/neo-bend-reality/wiz/-/releases)

## Wiki

Project notes and guides live here:

- [Wiki](https://gitlab.com/neo-bend-reality/wiz/-/wikis/home)

## Usage

Current behavior includes `help`, `list`, `add`, `delete`, `replace`, `run`,
and `export`.

```bash
wiz help
wiz list
wiz add build "python -m pytest -q"
wiz run build
wiz export
wiz delete build
wiz replace build "python -m pytest"
wiz --no-color list
wiz --version
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

## Packaging

To unpack the installer, you require the [7-Zip tool](https://www.7-zip.org/download.html).

## Contributing

See `CONTRIBUTING.md`.

## License

MIT. See `LICENSE`.
