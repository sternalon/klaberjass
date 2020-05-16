import random
import math

class GameConfig():

    def __init__(self, name):
        self.name = name
        self.deck_type = "split"
        self.num_players = 4
        self.num_tricks = 8
        self.deck = CardDeck(self.deck_type, self.num_players)
        self.rules = JassRules


class Card(object):
    """ A playing card.  """
    suits = {"spade":0,"heart":1,"diamond":2, "club":3}
    numbers = {"ace":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, "ten":10, "jack":11, "queen":12, "king":13}

    def __init__(self, number, suit):
        self.suit = suit
        self.number = number
        self.card_number = self.as_number()

    def as_number(self):
        """ returns a number from 1 (Ace of Clubs) and 52 (King of Spades)."""
        return self.number_rank() + self.suit_rank() * 13

    def suit_rank(self):
        if self.suit in Card.suits.keys():
            return Card.suits[self.suit]
        else:
            raise Exception(f"Invalid Suit: {self.suit}")

    def number_rank(self):
        if self.number in Card.numbers.keys():
            return Card.numbers[self.number]
        else:
            raise Exception(f"Invalid Number: {self.number}")

    def number_to_card(value):
        suits_reversed =  dict(zip(Card.suits.values(),Card.suits.keys()))
        numbers_reversed = dict(zip(Card.numbers.values(),Card.numbers.keys()))
        suit_val = math.ceil((value)/13) - 1
        number_val = value - (suit_val*13)
        suit = suits_reversed[suit_val]
        number = numbers_reversed[number_val]
        return Card(number, suit)

    def __str__(self):
        return f"{self.number} of {self.suit}"

    def __repr__(self):
        return f"{self.number} of {self.suit}"


class CardDeck():

    def __init__(self, deck_type, num_players):
        """Create a list of playing cards in our database"""
        suits = ["spade", "heart", "diamond", "club"]
        numbers = self.get_numbers(deck_type)
        self.cards = [Card(suit=suit, number=number) for number in numbers for suit in suits]
        self.num_players = num_players

    def get_numbers(self, deck_type):
        if deck_type =="split":
            return ["seven", "eight", "nine", "ten", "jack", "queen", "king", "ace"]
        if deck_type =="full":
            return ["two", "three","four", "five" , "six", "seven", "eight", "nine", "ten", "jack", "queen", "king", "ace"]
        else:
            raise Exception("Invalid Deck type")

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        self.shuffle()
        num_cards = len(self.cards)
        num_hand = int(num_cards/self.num_players)
        return [self.cards[i: i + num_hand] for i in range(0, num_cards, num_hand)]


class JassRules():
    rank = {"seven": 1, "eight": 2, "nine": 3, "jack": 4, "queen": 5, "king": 6, "ten": 7,  "ace": 8}
    trump_rank = {"seven": 11, "eight": 12, "queen": 13, "king": 14, "ten": 15,  "ace": 16, "nine": 17, "jack": 18}
    value = {"seven": 0, "eight": 0, "nine": 0, "jack": 2, "queen": 3, "king": 4, "ten": 10, "ace": 11}
    trump_value = {"seven": 0, "eight": 0, "queen": 3, "king": 4, "ten": 10, "ace": 11, "nine": 14, "jack": 20}

    def __init__(self, hand, trick, trump):
        self.hand = hand
        self.trick = trick
        self.trump = trump
        self.leading_suit = self.get_leading_suit()
        self.void = self.get_void(self.leading_suit)
        self.trick_trump = self.get_top_trump(self.trick)
        self.hand_trump = self.get_top_trump(self.hand)
        self.legal_cards = self.get_legal_cards()

    def get_rank_dict(self, trumps):
        if trumps:
            return JassRules.trump_rank
        else:
            return JassRules.rank

    def card_rank(self, card):
        """Returns card order for calculating which card is best"""
        rank_dict = self.get_rank_dict(self.is_trump(card))
        return rank_dict.get(card.number, 0)

    def card_value(self, card):
        """Returns card value used for adding score"""
        if self.is_trump(card):
            return JassRules.trump_value[card.number]
        else:
            return JassRules.value[card.number]

    def get_leading_suit(self):
        # TODO: A trick has a leading suit not the rules
        """Returns leading suit of the trick"""
        return self.trick[0].suit if self.trick else None

    def get_void(self, suit):
        # TODO: A hand should be void, not the rules
        """Returns whether the hand is void in suit"""
        return not any([card.suit == suit for card in self.hand])

    def is_trump(self, card):
        """Returns whether the card is a trump"""
        return card.suit == self.trump

    def is_better(self, card1, card2):
        """Returns whether the card1 beats card2"""
        return self.card_rank(card1) > self.card_rank(card2)

    def is_over_trump(self, card):
        # TODO: Needs to be tested
        """Returns whether card is an over trump (False if card is not a trump. True if no trumps in trick)"""
        return self.is_trump(card) and self.is_better(card, self.trick_trump)

    def get_trumps(self, cards):
        # TODO: Could be generalized to get suit
        """Returns list of trumps from list of cards"""
        return [card for card in cards if self.is_trump(card)]

    def get_top_trump(self, cards):
        # TODO: Could be generalized to get any suit suit
        """Returns top trump from list of cards (None otherwise)"""
        rank_dict = self.get_rank_dict(trumps=True)
        trumps = [card for card in self.get_trumps(cards)]
        ranks = [rank_dict.get(trump.number) for trump in trumps]
        return trumps[ranks.index(max(ranks))] if ranks else None

    def can_overtrump(self):
        """Returns true if hand has a higher trump than the top trump in the trick"""
        return self.is_better(self.hand_trump, self.trick_trump)

    def get_legal_cards(self):
        return [card for card in self.hand if self.validate_play(card)[0] is True]

    def validate_play(self, card):
        """Returns whether card can be legally played"""

        if not self.rule_leading_suit(card):
            message = "Illegal move: you must play the leading suit."
            return False, message
        elif not self.rule_must_trump(card):
            message = "Illegal move: you must trump if you can."
            return False, message
        elif not self.rule_overtrump(card):
            message = "Illegal move: must over trump if you can"
            return False, message
        else:
            message = "Success"
            return True, message

    def rule_leading_suit(self, card):
        """Player must play leading suit if they can"""
        if self.trick:
            if not self.void:
                return card.suit == self.leading_suit
        return True


    def rule_must_trump(self, card):
        """If player is void, they must play trump if they can (unless they can't overtrump)"""
        if self.trick:
            if self.void and self.can_overtrump():
                return self.is_trump(card)
        return True

    def rule_overtrump(self, card):
        """Player must play over trump when trumps are lead or if they are void"""
        if self.trick:
            if ((self.trump == self.leading_suit) or self.void) and self.can_overtrump():
                return self.is_over_trump(card)
        return True