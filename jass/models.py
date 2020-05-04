from django.db import models
from django.contrib.auth.models import User
from .utils import Card
from .utils import GameConfig

# Create your models here.

class Series(models.Model):
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

class Game(models.Model):
    KLABBERJASS = 'klabberjass'
    GAMES = [(KLABBERJASS, 'Klabberjass')]
    SUITS = [("spade", 'Spade'), ("heart", 'Heart'), ("diamond", 'Diamond'), ("club", 'Club')]

    name = models.CharField(choices=GAMES, default=KLABBERJASS, max_length=12)
    completed = models.BooleanField(default=False)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True)
    trumps = models.CharField(choices=SUITS, max_length=7)
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
        return list(Player.objects.filter(game=self).order_by('position'))


    def _deal(self):
        config = GameConfig(self.name)
        deck = config.deck
        hands = deck.deal()
        self._assign_cards(hands)
        self._create_tricks(config.num_tricks)

    def _assign_cards(self, hands):
        players = self.get_players()
        if len(hands)!= len(players):
            raise Exception("Number of players does not match number of dealt hands")
        for k in range(len(players)):
            for card in hands[k]:
                PlayingCard.objects.create(card= card, game=self, player=players[k])

    def _create_tricks(self, num_tricks):
        for k in range(num_tricks):
            Trick.objects.create(game=self, number=k+1)

    def get_tricks(self):
        return list(Trick.objects.filter(game=self).order_by('number'))

    def get_current_trick(self):
        open_tricks = Trick.objects.filter(game=self, winner = None).order_by('number')
        if len(open_tricks)>0:
            return open_tricks[0]
        else:
            return None


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.SmallIntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def get_hand(self):
        return list(PlayingCard.objects.filter(game=self.game, player=self))

    def get_unplayed_hand(self):
        return list(PlayingCard.objects.filter(game=self.game, player=self, played=False ))


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

class Trick(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, null = True)
    number = models.SmallIntegerField()

    def to_play(self):
        lead_position = self.lead().position
        num_cards_in_trick = len(self.cards())
        position = self.mod_num_player(lead_position + num_cards_in_trick)
        return Player.objects.get(game = self.game, position = position)

    def mod_num_player(self, number):
        num_players = len(self.game.get_players())
        if number > num_players:
            number = number - num_players
        return number

    def cards(self):
        return PlayingCard.objects.filter(trick=self).order_by('order_in_trick')

    def num_cards_played(self):
        return len(self.cards())

    def lead(self):
        if self.number == 1:
            # TODO: currently set up that player 1 leads. This could be done differently.
            return Player.objects.get(game=self.game, position = 1)
        else:
            previous_trick = Trick.objects.get(game=self.game, number = self.number -1)
            return previous_trick.winner



class PlayingCard(models.Model):
    card = CardField()
    played = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    trick = models.ForeignKey(Trick, on_delete=models.SET_NULL, null=True)
    order_in_trick = models.SmallIntegerField(null=True)

    class Meta:
        unique_together = ('card', 'game',)


    def play(self, trick):
        valid, message = self.valid_play(trick)
        if valid:
            self.trick = trick
            self.order_in_trick = trick.num_cards_played() + 1
            self.played = True
            self.save()
        return valid, message


    def valid_play(self, trick):
        # TODO: Move the first checks to the view validation?
        if not self._validate_game(trick):
            message = "Invalid Play: Card belongs to incorrect game"
            return False, message
        if not self._not_played():
            message = "Invalid Play: Card has already been played"
            return False, message
        if not self._validate_turn(trick):
            message = "Invalid Play: Card played in incorrect order"
            return False, message

        card = self.card
        hand = self.player.get_unplayed_hand()
        # valid , message = game.Rules.valid_play(playing_card.card, )
        return self._validate_card(card, hand)


    def _validate_game(self, trick):
        return self.game == trick.game

    def _not_played(self):
        return (not self.played)

    def _validate_turn(self, trick):
        return self.player == trick.to_play()

        return (player_position==turn_position)

    def _validate_card(self, card, hand):
        # TODO: Implement actual Jass rules.?
        return True , "Success"



class Bid(models.Model):
    SUITS = [("spade", 'Spade'), ("heart", 'Heart'), ("diamond", 'Diamond'), ("club", 'Club')]
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    play = models.BooleanField()
    suit = models.CharField(choices=SUITS, max_length=7)




