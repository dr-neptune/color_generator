from rich.console import Console
from rich.text import Text
from rich.style import Style
import random

from typing import List, Optional

from common import EXAMPLE_COLORS, EXTENDED_COLORS

def terminal_palette(color_palette: List[str], message: Optional[str] = None):
    """
    prints a color palette in the terminal

    Args:
        color_palette: A list of hex_codes to show in the terminal
        message: A message to display over the palette

    Side Effect:
        prints to the terminal
    """
    bars, hex_names = [], []

    for color in color_palette:
        bars.append(Text(" " * 9, style=Style(bgcolor=color)))
        hex_names.append(Text(f" {color} ", style=Style(color=color)))

    console = Console()
    console.print(Text(message), style=Style(color=random.choice(color_palette),
                                             bold=True))
    console.print(*bars)
    console.print(*hex_names)


if __name__ == '__main__':
    terminal_palette(color_palette=EXAMPLE_COLORS,
                     message="Here is the initial color palette!")

    terminal_palette(color_palette=EXTENDED_COLORS,
                     message="Here is the updated color palette!")
