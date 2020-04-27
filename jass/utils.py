import random
import math

class GameConfig():

    def __init__(self, name):
        self.name = name
        self.deck_type = "split"
        self.num_players = 4
        self.deck = CardDeck(self.deck_type, self.num_players)


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