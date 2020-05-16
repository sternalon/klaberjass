from django.test import TestCase

from ..utils import Card, CardDeck, GameConfig, JassRules


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


class JassRulesTest(TestCase):

    def setUp(self):
        self.ace_spades = Card(number="ace", suit="spade")
        self.king_spades = Card(number="king", suit="spade")
        self.jack_spades = Card(number="king", suit="spade")
        self.ace_hearts = Card(number="ace", suit="heart")
        self.king_hearts = Card(number="king", suit="heart")
        self.queen_hearts = Card(number="king", suit="heart")
        self.jack_hearts = Card(number="jack", suit="heart")
        self.nine_hearts = Card(number="nine", suit="heart")
        self.ace_clubs = Card(number="ace", suit="club")

    def test_jass_rules_methods(self):
        """
        Test KlabberJass rules class
        """

        hand = [self.ace_spades, self.king_spades, self.jack_hearts, self.nine_hearts, self.queen_hearts]
        trick = [self.ace_hearts, self.king_hearts]
        rules = JassRules(hand, trick, trump="heart")

        #Testing card_ranks
        self.assertIs(rules.card_rank(self.ace_spades), 8)
        self.assertIs(rules.card_rank(self.ace_hearts), 16)
        self.assertIs(rules.card_rank(self.nine_hearts), 17)
        self.assertIs(rules.card_rank(self.jack_hearts), 18)

        # Testing card_value
        self.assertIs(rules.card_value(self.ace_spades), 11)
        self.assertIs(rules.card_value(self.ace_hearts), 11)
        self.assertIs(rules.card_value(self.nine_hearts), 14)
        self.assertIs(rules.card_value(self.jack_hearts), 20)

        # Testing leading suit
        self.assertIs(rules.leading_suit, "heart")

        #Testing get_void method
        self.assertFalse(rules.void)
        self.assertTrue(rules.get_void("club"))

        # Test is_trumps
        self.assertFalse(rules.is_trump(self.ace_spades))
        self.assertTrue(rules.is_trump(self.ace_hearts))

        # Test is better
        self.assertTrue(rules.is_better(self.ace_spades, self.jack_spades))
        self.assertFalse(rules.is_better(self.ace_hearts, self.jack_hearts))
        self.assertTrue(rules.is_better(self.nine_hearts, self.ace_hearts))

        # Test get_trumps
        self.assertEqual(rules.get_trumps(hand), [self.jack_hearts, self.nine_hearts, self.queen_hearts])
        self.assertEqual(rules.get_trumps(trick), [self.ace_hearts, self.king_hearts])
        self.assertEqual(rules.get_trumps([]), [])

        # Test get_top_trumps
        self.assertEqual(rules.get_top_trump(hand), self.jack_hearts)
        self.assertEqual(rules.get_top_trump(trick), self.ace_hearts)

        # Test can_overtrump
        self.assertTrue(rules.can_overtrump())

    def test_leading_suit_not_trumps(self):
        """
        Test for which cards can be played when a non-trump is lead and player is not void
        Player should only be allowed to play leading suit.
        """

        hand = [self.ace_spades, self.jack_spades, self.ace_hearts, self.queen_hearts]
        trick = [self.king_spades, self.king_hearts]
        rules = JassRules(hand, trick, trump="heart")

        valid , message = rules.validate_play(self.ace_spades)
        self.assertTrue(valid)
        self.assertEqual(message, "Success")

        valid, message = rules.validate_play(self.jack_spades)
        self.assertTrue(valid)
        self.assertEqual(message, "Success")

        valid, message = rules.validate_play(self.ace_hearts)
        self.assertFalse(valid)
        self.assertEqual(message, "Illegal move: you must play the leading suit.")

        valid, message = rules.validate_play(self.queen_hearts)
        self.assertFalse(valid)
        self.assertEqual(message, "Illegal move: you must play the leading suit.")

    def test_leading_trumps(self):
        """
        Test of which cards can be played when a trump is lead and player is not void.
        Player must play a trump, and must overtrump.
        """

        hand = [self.ace_spades, self.jack_hearts, self.queen_hearts]
        trick = [self.ace_hearts, self.king_hearts]
        rules = JassRules(hand, trick, trump="heart")

        # Testing validate Play - leading card ace_hearts (trumps
        valid , message = rules.validate_play(self.ace_spades)
        self.assertFalse(valid)
        self.assertEqual(message, "Illegal move: you must play the leading suit.")

        valid, message = rules.validate_play(self.queen_hearts)
        self.assertFalse(valid)
        self.assertEqual(message, "Illegal move: must over trump if you can")

        valid, message = rules.validate_play(self.jack_hearts)
        self.assertTrue(valid)
        self.assertEqual(message, "Success")

    def test_lead_to_void_suit(self):
        """
        Test of which cards can be played when a non-trump is lead and player is void.
        Player must play a trump, and must over trump.
        """
        hand = [self.ace_spades, self.jack_hearts, self.queen_hearts]
        trick = [self.ace_clubs, self.king_hearts]
        rules = JassRules(hand, trick, trump="heart")

        valid, message = rules.validate_play(self.ace_spades)
        self.assertFalse(valid)
        self.assertEqual(message, "Illegal move: you must trump if you can.")

        valid, message = rules.validate_play(self.queen_hearts)
        self.assertFalse(valid)
        self.assertEqual(message, "Illegal move: must over trump if you can")

        valid, message = rules.validate_play(self.jack_hearts)
        self.assertTrue(valid)
        self.assertEqual(message, "Success")

    def test_lead_to_void_cant_overtrump(self):
        """
        Test of which cards can be played when a non-trump is lead and player is void, but can't overtrump.
        Player can play any card (ie: can play a trump or discard)
        """
        hand = [self.ace_spades, self.queen_hearts]
        trick = [self.ace_clubs, self.king_hearts]
        rules = JassRules(hand, trick, trump="heart")

        valid, message = rules.validate_play(self.ace_spades)
        self.assertTrue(valid)
        self.assertEqual(message, "Success")

        valid, message = rules.validate_play(self.queen_hearts)
        self.assertTrue(valid)
        self.assertEqual(message, "Success")

    def test_play_first_cards(self):
        """
        Test that a player can play any card when leading .
        Player can play any card (ie: can play a trump or discard)
        """
        hand = [self.ace_spades, self.queen_hearts]
        trick = []
        rules = JassRules(hand, trick, trump="heart")

        valid, message = rules.validate_play(self.ace_spades)
        self.assertTrue(valid)
        self.assertEqual(message, "Success")

        valid, message = rules.validate_play(self.queen_hearts)
        self.assertTrue(valid)
        self.assertEqual(message, "Success")