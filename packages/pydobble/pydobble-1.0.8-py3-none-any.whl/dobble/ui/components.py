from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from ..game.card import DobbleCard

console = Console()


def create_card_table(card: DobbleCard, show_coordinates: bool = True) -> Table:
    if not card:
        return Table()

    grid = card.get_symbol_grid()
    size = len(grid)

    table = Table(box=box.ROUNDED, show_header=show_coordinates, show_edge=False)

    if show_coordinates:
        table.add_column("")
        for i in range(size):
            table.add_column(chr(65 + i), justify="center")
    else:
        for i in range(size):
            table.add_column("", justify="center")

    for i, row in enumerate(grid):
        if show_coordinates:
            table_row = [str(i + 1)]
        else:
            table_row = []

        table_row.extend(emoji for _, emoji in row)
        table.add_row(*table_row)

    return table
