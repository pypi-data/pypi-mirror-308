from typing import List, Tuple, Optional
import random
from .card import DobbleCard
from .player import Player
from ..config import VALID_CARD_SIZES


class DobbleGame:
    def __init__(self, symbols_per_card: int):
        if symbols_per_card not in VALID_CARD_SIZES:
            valid_options = ", ".join(str(x) for x in VALID_CARD_SIZES)
            raise ValueError(
                f"Invalid number of symbols per card. Must be one of: {valid_options}"
            )

        self.symbols_per_card = symbols_per_card
        self.cards = self._generate_cards()
        self.live_card: Optional[DobbleCard] = None
        self.players: List[Player] = []

    def _generate_cards(self) -> List[DobbleCard]:
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

    def find_matching_players(self, coordinate: str) -> List[int]:
        try:
            col = ord(coordinate[0].upper()) - ord("A")
            row = int(coordinate[1:]) - 1

            if not self.live_card:
                return []

            grid = self.live_card.get_symbol_grid()
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                target_symbol = grid[row][col][0]
                if target_symbol is None:
                    return []

                return [
                    i
                    for i, player in enumerate(self.players)
                    if player.get_card() and target_symbol in player.get_card().symbols
                ]
        except (IndexError, ValueError):
            pass

        return []

    def process_claim(
        self, coordinate: str, winner_idx: int
    ) -> Tuple[bool, Optional[str]]:
        matching_players = self.find_matching_players(coordinate)
        if winner_idx in matching_players:
            player = self.players[winner_idx]
            card = player.remove_top_card()
            if card:
                self.live_card = card
                return True, player.name
        return False, None
