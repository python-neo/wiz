from argparse import ArgumentParser, REMAINDER
from textwrap import dedent
from pathlib import Path
from json import dump, load

HELP_TEXT = dedent (
    """
    Usage:
        wiz <command> <options>
    Commands:
        add             Add an alias to the manager
        delete          Delete an alias from the manager
        run             Run given alias
        list            List all aliases
        help            Show help for commands
        replace         Replaces an alias with another one.
    """).strip ()

class Commands :
    def __init__ (self) :
        self.commands = {
            "list" : {"func" : self.list, "subcmd" : False, "rest" : False},
            "help" : {"func" : self.help, "subcmd" : False, "rest" : False},
            "add" : {"func" : self.add, "subcmd" : True, "rest" : True},
            "replace" : {"func" : self.replace, "subcmd" : True, "rest" : True}
        }
        self.BASE_DIR = Path (__file__).resolve ().parent
        self.config_path = self.BASE_DIR / "config.json"
        self.aliases = {}

        if not self.config_path.exists () :
            self.write_config ()
        with open (self.config_path, "r") as f :
            self.aliases : dict = load (f)

    def list (self) :
        if not self.aliases :
            print ("No aliases yet.")
            return
        for alias, command in self.aliases.items () :
            print (f"{alias}        {command}")

    def replace (self, alias, command) :
        self.aliases [alias] = command
        self.write_config ()

    def help (self) :
        print (HELP_TEXT)

    def add (self, alias, command) :
        if alias in self.aliases.keys () :
            print (f"ERROR: {alias} already exists.")
            return
        self.aliases [alias] = command
        self.write_config ()

    def write_config (self) :
        with open (self.config_path, "w") as f :
            dump (self.aliases, f, indent = 4)

def parse_tokens (tokens) :
    if not tokens :
        return "help", None, ""
    command = tokens [0].strip () or "help"
    subcmd = tokens [1] if len (tokens) > 1 else None
    rest = " ".join (tokens [2:])
    return command, subcmd, rest

def run_command (commands, command, subcmd, rest) :
    entry = commands.commands.get (command)

    if entry is None :
        print (f"ERROR: unknown command '{command}'")
        return

    if not entry ["subcmd"] :
        entry ["func"] ()
        return
    if not subcmd :
        print (f"ERROR: '{command}' missing arguments.")
        return
    if entry ["rest"] :
        if not rest :
            print (f"ERROR: '{command}' missing arguments.")
            return
        entry ["func"] (subcmd, rest)
    else :
        entry ["func"] (subcmd)

if __name__ == "__main__" :
    commands = Commands ()
    argparser = ArgumentParser (add_help = False)
    argparser.add_argument ("command", nargs = REMAINDER)
    args = argparser.parse_args ()

    tokens = args.command
    command, subcmd, rest = parse_tokens (tokens)
    run_command (commands, command, subcmd, rest)