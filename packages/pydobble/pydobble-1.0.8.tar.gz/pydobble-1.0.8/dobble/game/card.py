from dataclasses import dataclass
from typing import List, Set, Tuple, Optional
import math
from ..utils.emoji_loader import EMOJI_MAP


@dataclass
class DobbleCard:
    symbols: Set[int]

    def __str__(self) -> str:
        emoji_symbols = [EMOJI_MAP[s % len(EMOJI_MAP)] for s in sorted(self.symbols)]
        return f"Card({', '.join(emoji_symbols)})"

    def get_symbol_grid(self) -> List[List[Tuple[Optional[int], str]]]:
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

    def get_matching_symbol(self, other: "DobbleCard") -> Optional[Tuple[int, str]]:
        matching_symbols = self.symbols & other.symbols
        if not matching_symbols:
            return None
        matching_num = next(iter(matching_symbols))
        return matching_num, EMOJI_MAP[matching_num % len(EMOJI_MAP)]
