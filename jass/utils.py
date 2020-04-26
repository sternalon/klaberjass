import random

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

    def __str__(self):
        return f"{self.number} of {self.suit}"
        return f"{str(self.number_rank()) }"

    def __repr__(self):
        return str(self)


class JasDeck():

    def __init__(self):
        """Create a list of playing cards in our database"""
        suits = ["spade", "heart", "diamond", "club"]
        numbers = ["seven", "eight", "nine", "ten", "jack", "queen", "king", "ace"]
        self.cards = [Card(suit=suit, number=number) for number in numbers for suit in suits]
        # self.cards = [(suit, rank) for rank in ranks for suit in suits]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_players = 4):
        self.shuffle()
        num_cards = len(self.cards)
        num_hand = int(num_cards/num_players)
        return [self.cards[i: i + num_hand] for i in range(0, num_cards, num_hand)]