from django.test import TestCase

from ..utils import Card, CardDeck, GameConfig


class CardTests(TestCase):

    def test_cards_class(self):
        """
        Test that Deck works correctly.
        """

        two_spades = Card(number = "two", suit = "spade")
        self.assertIs(two_spades.suit, "spade")
        self.assertIs(two_spades.number, "two")
        self.assertIs(two_spades.number_rank(), 2)
        self.assertIs(two_spades.suit_rank(), 0)
        self.assertIs(two_spades.as_number(), 2)
        card = Card.number_to_card(two_spades.as_number())
        self.assertEqual(card.number, two_spades.number)
        self.assertEqual(card.suit, two_spades.suit)

        five_clubs = Card(number="five", suit="club")
        self.assertIs(five_clubs.suit, "club")
        self.assertIs(five_clubs.number, "five")
        self.assertIs(five_clubs.number_rank(), 5)
        self.assertIs(five_clubs.suit_rank(), 3)
        self.assertIs(five_clubs.as_number(), 44)
        card = Card.number_to_card(five_clubs.as_number())
        self.assertEqual(card.number, five_clubs.number)
        self.assertEqual(card.suit, five_clubs.suit)

        king_hearts = Card(number="king", suit="heart")
        self.assertIs(king_hearts.suit, "heart")
        self.assertIs(king_hearts.number, "king")
        self.assertIs(king_hearts.number_rank(), 13)
        self.assertIs(king_hearts.suit_rank(), 1)
        self.assertIs(king_hearts.as_number(), 26)
        card = Card.number_to_card(king_hearts.as_number())
        self.assertEqual(card.number, king_hearts.number)
        self.assertEqual(card.suit, king_hearts.suit)

        with self.assertRaises(Exception):
            Card(number="Bad_number", suit="club")
        with self.assertRaises(Exception):
            Card(number="five", suit="Bad_suit")



class DeckTests(TestCase):

    def test_create_deck(self):
        """
        Test that Deck works correctly.
        """
        deck = CardDeck("split", 4)
        self.assertIs(len(deck.cards), 32)

        deck.shuffle()
        self.assertIs(len(deck.cards), 32)

        # Verify that deal is working as expected.
        hands = deck.deal()
        cards =[]
        self.assertIs(len(hands), 4)
        for hand in hands:
            cards.extend(hand)
            self.assertIs(len(hand), 8)

        # Verify that all cards are present.
        self.assertIs(len(set(cards)), 32)

class GameConfigTEST(TestCase):

    def test_create_deck(self):
        """
        Test KlabberJass deck has the correct config.
        """
        config = GameConfig("Klabberjas")
        self.assertIs(config.num_players, 4)
        self.assertIs(config.deck_type, "split")

