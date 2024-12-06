import random
import sys
import math
from dataclasses import dataclass
from typing import List, Set, Tuple, Dict, Optional
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.columns import Columns
from rich.style import Style
from rich.text import Text
from rich import box


VALID_CARD_SIZES = [2, 3, 4, 6, 8, 12, 14, 18, 20, 24, 30, 32, 38, 42, 44, 48, 54, 60]
DIFFICULTY_LEVELS = {"Trivial": 3, "Easy": 4, "Normal": 8, "Hard": 12, "Extreme": 18}

console = Console()


def parse_code_points(line: str) -> list[int]:
    """
    Parse a line from the emoji file into code points.
    Handles both single values and ranges (e.g., '231A' or '2614..2615')
    """
    if ".." in line:
        start, end = line.split("..")
        return list(range(int(start, 16), int(end, 16) + 1))
    return [int(line, 16)]


def generate_emoji_map() -> Dict[int, str]:
    """
    Generate a mapping of numbers to Unicode emojis using code points from emojis.txt.

    Returns:
        Dict[int, str]: A dictionary mapping integer indices to Unicode emoji characters.
        The emojis are randomly shuffled to ensure different games have different symbols.
    """
    emojis = []

    emoji_file = Path(__file__).parent / "emojis.txt"

    with open(emoji_file, "r") as f:
        for line in f:
            line = line.strip()

            for code_point in parse_code_points(line):
                try:
                    emoji = chr(code_point)
                    if sys.stdout.encoding.upper() in ["UTF-8", "UTF8"]:
                        emoji.encode("utf-8")
                        emojis.append(emoji)
                except (UnicodeEncodeError, UnicodeError):
                    continue

    random.shuffle(emojis)
    return {i: emoji for i, emoji in enumerate(emojis)}


EMOJI_MAP = generate_emoji_map()


@dataclass
class Player:
    """
    Represents a player in the Dobble game.

    Attributes:
        name (str): The player's name.
        cards (List[DobbleCard]): The player's deck of cards.
    """

    name: str
    cards: List["DobbleCard"]

    def __str__(self) -> str:
        return f"{self.name} ({len(self.cards)} cards)"

    def get_card(self) -> "DobbleCard":
        return self.cards[0]

    def remove_top_card(self) -> "DobbleCard":
        return self.cards.pop(0)


@dataclass
class DobbleCard:
    """
    Represents a game card.

    Each card contains a set of symbols with exactly one symbol that matches
    any other given card. Symbols are represented by integers.

    Attributes:
        symbols (Set[int]): Set of integer symbols on the card.
    """

    symbols: Set[int]

    def __str__(self) -> str:
        emoji_symbols = [EMOJI_MAP[s % len(EMOJI_MAP)] for s in sorted(self.symbols)]
        return f"Card({', '.join(emoji_symbols)})"

    def get_symbol_grid(self) -> List[List[Tuple[int, str]]]:
        """
        Convert the card's symbols into a grid layout for display.

        Returns:
            List[List[Tuple[int, str]]]: A 2D grid where each cell contains
            a tuple of (symbol_number, emoji_character). Empty cells contain (None, " ").
        """
        symbols = sorted(self.symbols)
        size = math.ceil(math.sqrt(len(symbols)))
        grid = []
        idx = 0
        for i in range(size):
            row = []
            for j in range(size):
                if idx < len(symbols):
                    symbol = symbols[idx]
                    emoji = EMOJI_MAP[symbol % len(EMOJI_MAP)]
                    row.append((symbol, emoji))
                else:
                    row.append((None, " "))
                idx += 1
            grid.append(row)
        return grid

    def get_matching_symbol(self, other: "DobbleCard") -> Tuple[int, str]:
        """
        Find the matching symbol between this card and another card.

        Args:
            other (DobbleCard): The other card to compare with.

        Returns:
            Tuple[int, str]: A tuple of (symbol_number, emoji_character) if a match is found,
            None otherwise.
        """
        matching_symbols = self.symbols & other.symbols
        matching_num = next(iter(matching_symbols))
        return matching_num, EMOJI_MAP[matching_num % len(EMOJI_MAP)]


class DobbleGame:
    """
    Manages the core game logic for Dobble.

    The game involves players finding matching symbols between their cards and a central card.

    Attributes:
        symbols_per_card (int): Number of symbols on each card.
        cards (List[DobbleCard]): All cards in the game.
        live_card (DobbleCard): The current central card.
        players (List[Player]): List of players in the game.
    """

    def __init__(self, symbols_per_card: int):
        """
        Initialise a new Dobble game.

        Args:
            symbols_per_card (int): Number of symbols to put on each card.
                                Must be one of the values in VALID_CARD_SIZES.

        Raises:
            ValueError: If symbols_per_card is not in VALID_CARD_SIZES.
        """
        if symbols_per_card not in VALID_CARD_SIZES:
            valid_options = ", ".join(str(x) for x in VALID_CARD_SIZES)
            raise ValueError(
                f"Invalid number of symbols per card. Must be one of: {valid_options}"
            )

        self.symbols_per_card = symbols_per_card
        self.cards = self._generate_cards()
        self.live_card: DobbleCard
        self.players: List[Player] = []

    def _generate_cards(self) -> List[DobbleCard]:
        """
        Generate a complete set of Dobble cards ensuring each pair of cards shares exactly one symbol.

        Returns:
            List[DobbleCard]: The generated set of cards.
        """
        n = self.symbols_per_card - 1
        cards = (
            [[i + n**2 for i in range(n + 1)]]
            + [[(o + i * n) for i in range(n)] + [n + n**2] for o in range(n)]
            + [
                [(o * n + i * (p * n + 1)) % (n**2) for i in range(n)] + [p + n**2]
                for p in range(n)
                for o in range(n)
            ]
        )
        return [DobbleCard(set(card)) for card in cards]

    def setup_game(self, player_names: List[str]) -> None:
        """
        Set up the game for the given players.

        Args:
            player_names (List[str]): Names of players to set up the game for.

        Raises:
            ValueError: If no player names are provided.
        """
        if not player_names:
            raise ValueError("Must provide at least one player name")

        shuffled_cards = self.cards.copy()
        random.shuffle(shuffled_cards)

        self.live_card = shuffled_cards.pop()

        cards_per_player = len(shuffled_cards) // len(player_names)

        self.players = []
        for i, name in enumerate(player_names):
            start_idx = i * cards_per_player
            end_idx = start_idx + cards_per_player
            player_cards = shuffled_cards[start_idx:end_idx]
            self.players.append(Player(name=name, cards=player_cards))

    def create_card_table(
        self, card: DobbleCard, show_coordinates: bool = True
    ) -> Table:
        """
        Create a rich Table representation of a card.

        Args:
            card (DobbleCard): The card to create a table for.
            show_coordinates (bool): Whether to show coordinate labels (A1, B2, etc.).

        Returns:
            Table: A rich Table object representing the card.
        """
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

    def display_game_state(self) -> None:
        """Display the current game state, including the live card and all players' top cards."""
        console.clear()

        console.print(
            Panel(
                self.create_card_table(self.live_card, show_coordinates=True),
                title="[cyan]Live Card[/cyan]",
                border_style="cyan",
                expand=False,
            )
        )

        player_panels = []
        for player in self.players:
            top_card = player.get_card()
            if top_card:
                card_table = self.create_card_table(top_card, show_coordinates=False)
                player_panels.append(
                    Panel(
                        card_table,
                        title=f"[bold]{player.name}[/bold] ({len(player.cards)} cards)",
                        border_style="green",
                    )
                )

        console.print(Columns(player_panels, equal=True, expand=True))

    def find_all_matching_players(self, coordinate: str) -> List[int]:
        """
        Find all players whose top cards match the symbol at the given coordinate.

        Args:
            coordinate (str): The coordinate to check (e.g., 'A1', 'B2').

        Returns:
            List[int]: Indices of all players with matching cards.
        """
        try:
            col = ord(coordinate[0].upper()) - ord("A")
            row = int(coordinate[1:]) - 1

            grid = self.live_card.get_symbol_grid()
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                target_symbol = grid[row][col][0]
                if target_symbol is None:
                    return []

                matching_players = []
                for i, player in enumerate(self.players):
                    player_card = player.get_card()
                    if player_card and target_symbol in player_card.symbols:
                        matching_players.append(i)
                return matching_players
        except (IndexError, ValueError):
            pass

        return []

    def select_matching_player(self, matching_players: List[int]) -> int:
        """
        Prompt the user to select which player spotted the match first.

        Args:
            matching_players (List[int]): List of indices of players with matching cards.

        Returns:
            int: Index of the selected player.
        """
        if len(matching_players) == 1:
            return matching_players[0]

        console.print("\n[yellow]More than one player has that symbol![/yellow]")
        console.print("Who spotted the match first?")

        for i, player_idx in enumerate(matching_players, 1):
            console.print(f"{i}. {self.players[player_idx].name}")

        while True:
            choice = IntPrompt.ask(
                "Enter player number",
                choices=[str(i) for i in range(1, len(matching_players) + 1)],
            )
            if 1 <= choice <= len(matching_players):
                return matching_players[choice - 1]

    def process_claim(self, coordinate: str) -> Tuple[bool, Optional[str]]:
        """
        Process a player's claim of having found a matching symbol.

        Args:
            coordinate (str): The 'live card' coordinate of the symbol claimed as a match (e.g., 'A1', 'B2').

        Returns:
            Tuple[bool, Optional[str]]: A tuple containing:
                - bool: Whether the claim was valid
                - Optional[str]: The name of the player who made the successful claim
                                 (either inferred, or clarified by the user where multiple
                                 players hold the symbol)
        """
        matching_players = self.find_all_matching_players(coordinate)
        if matching_players:
            selected_player_idx = self.select_matching_player(matching_players)
            player = self.players[selected_player_idx]
            self.live_card = player.remove_top_card()
            return True, player.name

        return False, None


def display_title():
    title = """[cyan]
╔╦╗╔═╗╔╗ ╔╗ ╦  ╔═╗
 ║║║ ║╠╩╗╠╩╗║  ║╣
═╩╝╚═╝╚═╝╚═╝╩═╝╚═╝
[/cyan]"""
    console.print(title, justify="center")

def get_arrow_key_selection(options: List[str], display_func) -> int:
    """
    Handle arrow key selection from a list of options.

    Args:
        options: List of options to choose from
        display_func: Function to display the current state

    Returns:
        Selected index
    """
    import sys
    import tty
    import termios

    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                ch = sys.stdin.read(2)
                return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    current_selection = 0

    while True:
        console.clear()
        display_func(current_selection)

        key = get_key()

        if key == "[A":  # Up arrow
            current_selection = (current_selection - 1) % len(options)
        elif key == "[B":  # Down arrow
            current_selection = (current_selection + 1) % len(options)
        elif key == "\r":  # Enter key
            return current_selection


def display_difficulty_options(current_selection: int) -> None:
    """Display difficulty options in a table format with the current selection highlighted."""
    display_title()

    console.print(
        "\n[bold yellow]Select Difficulty (Use ↑↓ arrows, Enter to select):[/bold yellow]\n"
    )

    table = Table(box=box.ROUNDED, show_header=True)
    table.add_column("Difficulty Level", style="cyan")
    table.add_column("Symbols per Card", justify="center", style="green")

    for i, (level, size) in enumerate(DIFFICULTY_LEVELS.items()):
        if i == current_selection:
            style = Style(bgcolor="blue", color="white")
            level_text = Text(level, style=style)
            size_text = Text(str(size), style=style)
        else:
            level_text = Text(level)
            size_text = Text(str(size))
        table.add_row(level_text, size_text)

    # Add Custom option
    if current_selection == len(DIFFICULTY_LEVELS):
        style = Style(bgcolor="blue", color="white")
        custom_text = Text("Custom", style=style)
        custom_size = Text("Choose your own", style=style)
    else:
        custom_text = Text("Custom")
        custom_size = Text("Choose your own")
    table.add_row(custom_text, custom_size)

    console.print(table)


def select_difficulty() -> int:
    options = list(DIFFICULTY_LEVELS.keys()) + ["Custom"]
    selection = get_arrow_key_selection(options, display_difficulty_options)

    if selection < len(DIFFICULTY_LEVELS):
        return list(DIFFICULTY_LEVELS.values())[selection]
    else:
        console.clear()
        display_title()
        valid_sizes = ", ".join(map(str, VALID_CARD_SIZES))
        console.print(f"\nValid card sizes: {valid_sizes}")
        while True:
            size = IntPrompt.ask("Enter number of symbols per card")
            if size in VALID_CARD_SIZES:
                return size
            console.print("[red]Invalid size. Please choose from the list above.[/red]")


def main():
    console.clear()
    display_title()

    symbols_per_card = select_difficulty()
    game = DobbleGame(symbols_per_card=symbols_per_card)

    player_names = Prompt.ask("Enter player names (comma-separated)").split(",")
    player_names = [name.strip() for name in player_names if name.strip()]

    game.setup_game(player_names)

    while True:
        game.display_game_state()

        coordinate = Prompt.ask("\nEnter coordinate (e.g., B3) or 'q' to quit")
        if coordinate.lower() == "q":
            break

        success, player_name = game.process_claim(coordinate)
        if success:
            console.print(f"[green]Well done {player_name}![/green]")
        else:
            console.print("[red]That's not right.[/red]")

        if any(not player.cards for player in game.players):
            console.print("\n[bold yellow]Game Over![/bold yellow]")
            for player in game.players:
                if not player.cards:
                    console.print(f"[green]{player.name} was the winner![/green]")
                else:
                    console.print(f"{player.name} had {len(player.cards)} cards left")
            break

        console.input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
