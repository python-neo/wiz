# Wiz

Wiz is a hacker-vibe, command-line shortcut manager. It lets you store frequently
used commands as named shortcuts and run them instantly from any terminal.

Status: pre-alpha. This repo is scaffolding and docs; the CLI is still being built.

## Why

Daily command friction adds up. Wiz aims to make your personal command palette
fast, searchable, and easy to audit.

## Planned Features

- Add, list, run, and remove shortcuts
- Store shortcuts in a local config file
- Export shortcuts as shell aliases
- Lightweight, no external dependencies

## CLI Contract (Draft)

These commands define the intended interface. Implementation will follow this
contract as closely as possible.

- `wiz add <name> <command>`
- `wiz list`
- `wiz run <name>`
- `wiz remove <name>`
- `wiz export`

Example usage:

```text
wiz add build "python -m pytest -q"
wiz add serve "python -m http.server 8000"
wiz list
wiz run build
```

## Config (Draft)

Wiz will store shortcuts in a simple JSON file in your user profile directory.
Exact path may change as the CLI solidifies.

Example format:

```json
{
  "build": "python -m pytest -q",
  "serve": "python -m http.server 8000"
}
```

## Project Layout

- `README.md` project overview
- `CHANGELOG.md` release notes
- `CONTRIBUTING.md` contribution guidelines
- `main/` CLI source code (in progress)

## Roadmap

- MVP CLI (add/list/run/remove)
- Export to shell aliases
- Search and tags
- Usage stats

## License

TBD
