from argparse import ArgumentParser, REMAINDER
from textwrap import dedent

HELP_TEXT = dedent (
    """
    Usage:
        wiz <command> <options>
    Commands:
        add             Add an alias to the manager
        delete          Delete an alias from the manager
        run             Run given alias
        help            Show help for commands
    """).strip ()

class Commands :
    def __init__ (self) :
        self.commands = {
            "help" : {"func" : self.help, "subcmd" : False, "rest" : False},
        }
        
    def help (self) :
        print (HELP_TEXT)

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
    if entry ["rest"] :
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
