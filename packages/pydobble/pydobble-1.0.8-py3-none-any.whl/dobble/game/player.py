from dataclasses import dataclass
from typing import List, Optional
from .card import DobbleCard


@dataclass
class Player:
    name: str
    cards: List[DobbleCard]

    def __str__(self) -> str:
        return f"{self.name} ({len(self.cards)} cards)"

    def get_card(self) -> Optional[DobbleCard]:
        return self.cards[0] if self.cards else None

    def remove_top_card(self) -> Optional[DobbleCard]:
        return self.cards.pop(0) if self.cards else None
