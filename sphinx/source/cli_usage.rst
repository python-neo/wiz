CLI Usage
============

This page documents every Wiz command and flag with examples.

Overview
--------

Wiz is a command-line shortcut manager. It stores commands as aliases and lets
you run, replace, delete, list, and export them.

Run from source:

.. code-block:: text

   pip install -r requirements.txt
   python -m main.main help

Flags
-----

--version
    Print the Wiz version and exit.

Example:

.. code-block:: text

   python -m main.main --version

--no-color
    Disable colored output for terminals that do not support ANSI colors.

Note: Because Wiz uses ``argparse`` with a remainder parser, flags must come
before the command.

Example:

.. code-block:: text

   python -m main.main --no-color list

Commands
--------

help
    Show the help menu.

Example:

.. code-block:: text

   python -m main.main help

list
    List all stored aliases.

Example:

.. code-block:: text

   python -m main.main list

add
    Add an alias and persist it to ``main/config.json``.

Usage:

.. code-block:: text

   python -m main.main add <alias> <command>

Example:

.. code-block:: text

   python -m main.main add build "python -m pytest -q"

delete
    Delete an existing alias.

Usage:

.. code-block:: text

   python -m main.main delete <alias>

Example:

.. code-block:: text

   python -m main.main delete build

replace
    Replace an alias with a new command.

Usage:

.. code-block:: text

   python -m main.main replace <alias> <command>

Example:

.. code-block:: text

   python -m main.main replace build "python -m pytest"

run
    Run an alias command. Wiz looks up the alias and executes the stored command.

Usage:

.. code-block:: text

   python -m main.main run <alias>

Example:

.. code-block:: text

   python -m main.main run build

Notes:

- If the command is not found in ``PATH``, Wiz will prompt for confirmation.

export
    Export aliases as shell commands.

Usage:

.. code-block:: text

   python -m main.main export

Output:

- On Windows CMD, prints ``doskey`` entries.
- On other shells, prints ``alias`` entries.
