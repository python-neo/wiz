from rich.console import Console
from rich.theme import Theme

theme = Theme ({
    "error" : "red",
    "success" : "green",
    "alias" : "magenta",
    "command" : "yellow"
})

def make_console (no_color : bool = False) -> Console :
    """
    Create a themed Rich console.

    Parameters :
        no_color (bool): Disable colored output when True.

    Returns :
        Console: Configured Rich console instance.
    """
    return Console (no_color = no_color, theme = theme)
