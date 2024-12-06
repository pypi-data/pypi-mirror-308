from typing import List
from rich.prompt import Prompt, IntPrompt
from .config import VALID_CARD_SIZES, DIFFICULTY_LEVELS
from .game.game import DobbleGame
from .ui.display import display_title, display_game_state
from .ui.input import get_arrow_key_selection, display_difficulty_options
from .ui.components import console


def select_difficulty() -> int:
    options = list(DIFFICULTY_LEVELS.keys()) + ["Custom"]
    selection = get_arrow_key_selection(options, display_difficulty_options)

    if selection < len(DIFFICULTY_LEVELS):
        return list(DIFFICULTY_LEVELS.values())[selection]

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
        display_game_state(game)

        coordinate = Prompt.ask("\nEnter coordinate (e.g., B3) or 'q' to quit")
        if coordinate.lower() == "q":
            break

        matching_players = game.find_matching_players(coordinate)
        if matching_players:
            if len(matching_players) == 1:
                winner_idx = matching_players[0]
            else:
                console.print(
                    "\n[yellow]More than one player has that symbol![/yellow]"
                )
                console.print("Who spotted the match first?")
                for i, player_idx in enumerate(matching_players, 1):
                    console.print(f"{i}. {game.players[player_idx].name}")

                while True:
                    choice = IntPrompt.ask(
                        "Enter player number",
                        choices=[str(i) for i in range(1, len(matching_players) + 1)],
                    )
                    if 1 <= choice <= len(matching_players):
                        winner_idx = matching_players[choice - 1]
                        break

            success, player_name = game.process_claim(coordinate, winner_idx)
            if success:
                console.print(f"[green]Well done {player_name}![/green]")
            else:
                console.print("[red]That's not right.[/red]")
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
