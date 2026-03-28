from rich.console import Console
from rich.theme import Theme

theme = Theme ({
    "error" : "red",
    "success" : "green",
    "alias" : "magenta",
    "command" : "yellow"
})

def make_console (no_color : bool = False) -> Console :
    return Console (no_color = no_color, theme = theme)
