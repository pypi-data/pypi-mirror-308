# test_dobble.py
import pytest
from dobble import DobbleGame, DobbleCard, Player, VALID_CARD_SIZES
import itertools

@pytest.mark.parametrize("symbols_per_card", VALID_CARD_SIZES)
def test_valid_card_generation(symbols_per_card):
    """Test that generated decks follow the rules of Dobble."""
    game = DobbleGame(symbols_per_card)

    # Test 1: Deck has the correct number of cards
    expected_cards = (symbols_per_card ** 2) - symbols_per_card + 1
    assert len(game.cards) == expected_cards

    # Test 2: Each card has the correct number of symbols
    for card in game.cards:
        assert len(card.symbols) == symbols_per_card

    # Test 3: Exactly one symbol matches for any two given cards
    for card1, card2 in itertools.combinations(game.cards, 2):
        common_symbols = card1.symbols & card2.symbols
        assert len(common_symbols) == 1

def test_invalid_symbols_per_card():
    """Test that invalid symbol counts are rejected."""
    invalid_counts = [5, 7, 9, 13, 15]
    for count in invalid_counts:
        with pytest.raises(ValueError):
            DobbleGame(count)

def test_player_creation():
    """Test player creation and card dealing."""
    game = DobbleGame(12)
    game.setup_game(["Alice", "Bob", "Charlie"])

    # Test equal card distribution
    cards_per_player = len(game.cards) // 3
    for player in game.players:
        assert len(player.cards) == cards_per_player

def test_player_remove_card():
    """Test player card removal mechanics."""
    game = DobbleGame(8)
    player = Player("Test", game.cards[:5])

    # Test playing cards reduces hand size
    initial_cards = len(player.cards)
    player.remove_top_card()
    assert len(player.cards) == initial_cards - 1

    # Test playing with empty hand
    for _ in range(len(player.cards)):
        player.remove_top_card()
    assert player.play_card() is None

def test_matching_symbols():
    """Test symbol matching between cards."""
    card1 = DobbleCard({1, 2, 3, 4, 5, 6, 7, 8})
    card2 = DobbleCard({1, 9, 10, 11, 12, 13, 14, 15})

    matching_num, matching_emoji = card1.get_matching_symbol(card2)
    assert matching_num == 1

if __name__ == "__main__":
    pytest.main([__file__])
