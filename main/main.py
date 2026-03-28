from argparse import ArgumentParser, REMAINDER
from textwrap import dedent
from pathlib import Path
from json import dump, load
from .console import make_console
from shutil import which
from subprocess import run as _run
from rich.prompt import Confirm

HELP_TEXT = dedent ("""
        Usage:
        [alias]wiz[/] [command]<command> <options>[/]

        Flags:
        [alias]--version[/]                      [command]Show version and exit[/]
        [alias]--no-color[/]                      [command]Disable colored output[/]

        Commands:
        [alias]add[/]                      [command]Add an alias to the manager[/]
        [alias]delete[/]                   [command]Delete an alias from the manager[/]
        [alias]export[/]                   [command]Export aliases for your shell[/]
        [alias]run[/]                      [command]Run given alias[/]
        [alias]list[/]                     [command]List all aliases[/]
        [alias]help[/]                     [command]Show help for commands[/]
        [alias]replace[/]                  [command]Replace an alias with another one[/]
    """).strip ()

class Commands :
    """
    Command handler for Wiz CLI operations.

    Loads alias config and dispatches supported commands.
    """
    def __init__ (self, no_color) -> None :
        """
        Initialize the command handler and load config.

        Parameters :
            no_color (bool): Disable colored output when True.

        Returns :
            None: Initializes internal state.
        """
        self.commands = {
            "list" : {"func" : self.list},
            "help" : {"func" : self.help},
            "add" : {"func" : self.add, "subcmd" : True, "rest" : True},
            "replace" : {"func" : self.replace, "subcmd" : True, "rest" : True},
            "delete" : {"func" : self.delete, "subcmd" : True},
            "run" : {"func" : self.run, "subcmd" : True},
            "export" : {"func" : self.export}
        }
        self.console = make_console (no_color = no_color)
        self.BASE_DIR : Path = Path (__file__).resolve ().parent
        self.config_path : Path = self.BASE_DIR / "config.json"
        self.aliases : dict = {}

        if not self.config_path.exists () :
            self.write_config ()
        with open (self.config_path, "r") as f :
            self.aliases = load (f)

    def add (self, alias : str, command : str) -> None :
        """
        Add a new alias and persist it.

        Parameters :
            alias (str): Alias name to add.
            command (str): Command string to store.

        Returns :
            None: Writes alias to config.
        """
        if alias in self.aliases.keys () :
            self.console.print (f"[error]ERROR[/]: '{alias}' already exists.")
            return
        self.aliases [alias] = command
        self.write_config ()
        self.console.print (f"[success]Successfully added alias '{alias}' to manager.[/]")

    def delete (self, alias : str) -> None :
        """
        Delete an existing alias and persist changes.

        Parameters :
            alias (str): Alias name to delete.

        Returns :
            None: Writes updated config.
        """
        if alias not in self.aliases :
            self.console.print (f"[error]ERROR[/]: '{alias}' does not exist.")
            return
        self.aliases.__delitem__ (alias)
        self.write_config ()
        self.console.print (f"[success]Successfully deleted alias '{alias}' from manager.[/]")

    def help (self) -> None :
        """
        Display the help menu.

        Returns :
            None: Prints help text.
        """
        self.console.print (HELP_TEXT)

    def export (self) -> None :
        """
        Export aliases to shell-friendly commands.

        Returns :
            None: Prints export output.
        """
        if not self.aliases :
            self.console.print ("[error]No aliases yet.[/]")
            return
        for alias, command in self.aliases.items () :
            self.console.print (f"doskey {alias}={command}")
            return

    def list (self) -> None :
        """
        List all stored aliases.

        Returns :
            None: Prints aliases or empty state.
        """
        if not self.aliases :
            self.console.print ("[error]No aliases yet.[/]")
            return
        for alias, command in self.aliases.items () :
            self.console.print (f"[alias]{alias}[/]                      [command]{command}[/]")

    def replace (self, alias : str, command : str) -> None :
        """
        Replace an alias with a new command.

        Parameters :
            alias (str): Alias name to replace.
            command (str): New command string.

        Returns :
            None: Writes updated config.
        """
        self.aliases [alias] = command
        self.write_config ()
        self.console.print (f"[success]Successfully replaced alias '{alias}' with command '{command}'.[/]")

    def run (self, alias : str) -> None :
        """
        Execute an alias command in the shell.

        Parameters :
            alias (str): Alias name to execute.

        Returns :
            None: Runs the command and reports errors.
        """
        if alias not in self.aliases :
            self.console.print (f"[error]ERROR[/]: '{alias}' does not exist.")
            return

        command : str = self.aliases [alias]

        exe = command.split () [0]
        if not which (exe) :
            confirm = Confirm.ask (f"[error]ERROR[/]: command '{command}' not found. Proceed anyway?")
            if not confirm :
                return

        result = _run (command, shell = True)
        if result.returncode != 0 :
            self.console.print (f"[error]ERROR[/]: command exited with {result.returncode}.")

    def write_config (self) -> None :
        """
        Persist aliases to the config file.

        Returns :
            None: Writes JSON to disk.
        """
        with open (self.config_path, "w") as f :
            dump (self.aliases, f, indent = 4)

def parse_tokens (tokens : list) -> tuple :
    """
    Parse raw CLI tokens into command, subcommand, and rest.

    Parameters :
        tokens (list): Tokenized CLI arguments.

    Returns :
        tuple: (command, subcmd, rest) parsed from tokens.
    """
    if not tokens :
        return "help", None, ""
    command = tokens [0].strip () or "help"
    subcmd = tokens [1] if len (tokens) > 1 else None
    rest = " ".join (tokens [2:])
    return command, subcmd, rest

def run_command (commands : Commands, command : str, subcmd : str | None, rest : str) -> None :
    """
    Dispatch parsed tokens to the correct command handler.

    Parameters :
        commands (Commands): Command handler instance.
        command (str): Primary command name.
        subcmd (str | None): Subcommand or alias name.
        rest (str): Remaining arguments string.

    Returns :
        None: Executes the command handler.
    """
    entry : dict = commands.commands.get (command, {})

    if not entry :
        commands.console.print (f"[error]ERROR[/]: unknown command '{command}'")
        return

    if not entry.get ("subcmd", False) :
        entry ["func"] ()
        return
    if not subcmd :
        commands.console.print (f"[error]ERROR[/]: '{command}' missing arguments.")
        return
    if entry.get ("rest", False) :
        if not rest :
            commands.console.print (f"[error]ERROR[/]: '{command}' missing arguments.")
            return
        entry ["func"] (subcmd, rest)
    else :
        if rest :
            commands.console.print (f"[error]ERROR:[/] {command} does not accept extra tokens.")
        entry ["func"] (subcmd)

if __name__ == "__main__" :
    argparser = ArgumentParser (add_help = False)
    argparser.add_argument ("--version", action = "version", version = "0.5.0", help = "Version for Wiz")
    argparser.add_argument ("--no-color", action = "store_true", help = "Color toggle for Wiz")
    argparser.add_argument ("command", nargs = REMAINDER, help = "Commands for Wiz")
    args = argparser.parse_args ()

    commands = Commands (no_color = args.no_color)
    tokens : list = args.command
    command, subcmd, rest = parse_tokens (tokens)
    run_command (commands, command, subcmd, rest)
