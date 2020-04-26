from django.test import TestCase

from .utils import Card, JasDeck

# Create your tests here.

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

        five_clubs = Card(number="five", suit="club")
        self.assertIs(five_clubs.suit, "club")
        self.assertIs(five_clubs.number, "five")
        self.assertIs(five_clubs.number_rank(), 5)
        self.assertIs(five_clubs.suit_rank(), 3)
        self.assertIs(five_clubs.as_number(), 44)

        with self.assertRaises(Exception):
            Card(number="Bad_number", suit="club")
        with self.assertRaises(Exception):
            Card(number="five", suit="Bad_suit")


class DeckTests(TestCase):

    def test_create_deck(self):
        """
        Test that Deck works correctly.
        """
        deck = JasDeck()
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