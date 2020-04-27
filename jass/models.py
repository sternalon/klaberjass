from django.db import models
from django.contrib.auth.models import User
from .utils import Card
from .utils import GameConfig

# Create your models here.


class Game(models.Model):
    KLABBERJASS = 'klabberjass'
    GAMES = [(KLABBERJASS, 'Klabberjass')]
    #
    name = models.CharField(choices=GAMES, default=KLABBERJASS, max_length=12)
    completed = models.BooleanField(default=False)
    # series = models.ForeignKey(Series)

    # dates
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def begin(self, users):
        self._set_players(users)
        self._deal()

    def _set_players(self, users):
        num_players = GameConfig(self.name).num_players
        if len(users)!= num_players:
            raise Exception(f"Error: Incorrect number of players: {len(users)} = {num_players}")
        position = 0
        for user in users:
            position += 1
            Player.objects.get_or_create(user=user, game=self, position = position)

    def get_players(self):
        return [player for player in Player.objects.filter(game=self).order_by('position')]

    def _deal(self):
        deck = GameConfig(self.name).deck
        hands = deck.deal()
        self._assign_cards(hands)

    def _assign_cards(self, hands):
        players = self.get_players()
        if len(hands)!= len(players):
            raise Exception("Number of players does not match number of dealt hands")
        for k in range(len(players)):
            for card in hands[k]:
                PlayingCard.objects.create(card= card, game=self, player=players[k])


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.SmallIntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def get_hand(self):
        return [card for card in PlayingCard.objects.filter(game=self.game, player=self)]


class CardField(models.PositiveIntegerField):

    def get_db_prep_value(self, value, connection, prepared=False):
        """Return the ``int`` equivalent of ``value``."""
        if value is None: return None
        try:
            int_value = value.as_number()
        except AttributeError:
            int_value = int(value)
        return int_value

    # def from_db_value(self, value, expression, connection, context):
    def from_db_value(self, value, expression, connection):

        """Return the ``Card`` equivalent of ``value``."""
        if value is None or isinstance(value, Card):
            return value
        return Card.number_to_card(value)

    # def to_python(self, value):
    #     """Return the ``Card`` equivalent of ``value``."""
    #     if value is None or isinstance(value, Card):
    #         return value
    #     return Card.number_to_card(value)

    # def get_prep_value(self, value):
    #     return ???



class PlayingCard(models.Model):
    card = CardField()
    played = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('card', 'game',)


# class Trick(models.Model):
#     game = models.ForeignKey(Game)
#     card1 = models.ForeignKey(PlayingCard)
#     card2 = models.ForeignKey(PlayingCard)
#     card3 = models.ForeignKey(PlayingCard)
#     card4 = models.ForeignKey(PlayingCard)
#     lead = models.ForeignKey(User)
#     winner = models.ForeignKey(User)
#     number = models.SmallIntegerField()
#
# class Set(models.Model):
#     player1 = models.ForeignKey(User)
#     player2 = models.ForeignKey(User)
#     player3 = models.ForeignKey(User)
#     player4 = models.ForeignKey(User)
#
#
#     score1 = models.IntegerField()
#     score2 = models.IntegerField()
#




