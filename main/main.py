from argparse import ArgumentParser, REMAINDER
from textwrap import dedent
from pathlib import Path
from json import dump, load
from .console import make_console

HELP_TEXT = dedent ("""
        Usage:
        [alias]wiz[/] [command]<command> <options>[/]

        Commands:
        [alias]add[/]                      [command]Add an alias to the manager[/]
        [alias]delete[/]                   [command]Delete an alias from the manager[/]
        [alias]run[/]                      [command]Run given alias[/]
        [alias]list[/]                     [command]List all aliases[/]
        [alias]help[/]                     [command]Show help for commands[/]
        [alias]replace[/]                  [command]Replace an alias with another one[/]
    """).strip ()

class Commands :
    def __init__ (self) -> None :
        self.commands = {
            "list" : {"func" : self.list, "subcmd" : False, "rest" : False},
            "help" : {"func" : self.help, "subcmd" : False, "rest" : False},
            "add" : {"func" : self.add, "subcmd" : True, "rest" : True},
            "replace" : {"func" : self.replace, "subcmd" : True, "rest" : True},
            "delete" : {"func" : self.delete, "subcmd" : True, "rest" : False}
        }
        self.console = make_console ()
        self.BASE_DIR : Path = Path (__file__).resolve ().parent
        self.config_path : Path = self.BASE_DIR / "config.json"
        self.aliases : dict = {}

        if not self.config_path.exists () :
            self.write_config ()
        with open (self.config_path, "r") as f :
            self.aliases = load (f)

    def add (self, alias : str, command : str) -> None :
        if alias in self.aliases.keys () :
            self.console.print (f"[error]ERROR[/]: '{alias}' already exists.")
            return
        self.aliases [alias] = command
        self.write_config ()
        self.console.print (f"[success]Successfully added alias '{alias}' to manager.[/]")

    def delete (self, alias : str) -> None :
        if alias not in self.aliases :
            self.console.print (f"[error]ERROR[/]: '{alias}' does not exist.")
            return
        self.aliases.__delitem__ (alias)
        self.write_config ()
        self.console.print (f"[success]Successfully deleted alias '{alias}' from manager.[/]")

    def help (self) -> None :
        self.console.print (HELP_TEXT)

    def list (self) -> None :
        if not self.aliases :
            self.console.print ("[error]No aliases yet.[/]")
            return
        for alias, command in self.aliases.items () :
            self.console.print (f"[alias]{alias}[/]                      [command]{command}[/]")

    def replace (self, alias : str, command : str) -> None :
        self.aliases [alias] = command
        self.write_config ()
        self.console.print (f"[success]Successfully replaced alias '{alias}' with command '{command}'.[/]")

    def write_config (self) -> None :
        with open (self.config_path, "w") as f :
            dump (self.aliases, f, indent = 4)

def parse_tokens (tokens : list) -> tuple :
    if not tokens :
        return "help", None, ""
    command = tokens [0].strip () or "help"
    subcmd = tokens [1] if len (tokens) > 1 else None
    rest = " ".join (tokens [2:])
    return command, subcmd, rest

def run_command (commands : Commands, command : str, subcmd : str | None, rest : str) -> None :
    entry = commands.commands.get (command)

    if entry is None :
        commands.console.print (f"[error]ERROR[/]: unknown command '{command}'")
        return

    if not entry ["subcmd"] :
        entry ["func"] ()
        return
    if not subcmd :
        commands.console.print (f"[error]ERROR[/]: '{command}' missing arguments.")
        return
    if entry ["rest"] :
        if not rest :
            commands.console.print (f"[error]ERROR[/]: '{command}' missing arguments.")
            return
        entry ["func"] (subcmd, rest)
    else :
        entry ["func"] (subcmd)

if __name__ == "__main__" :
    commands = Commands ()
    argparser = ArgumentParser (add_help = False)
    argparser.add_argument ("command", nargs = REMAINDER)
    args = argparser.parse_args ()

    tokens : list = args.command
    command, subcmd, rest = parse_tokens (tokens)
    run_command (commands, command, subcmd, rest)
