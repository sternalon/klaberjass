from django.db import models
from django.contrib.auth.models import User
from .utils import Card
from .utils import GameConfig

# Create your models here.

class Series(models.Model):
    KLABBERJASS = 'klabberjass'
    GAMES = [(KLABBERJASS, 'Klabberjass')]
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    game_type = models.CharField(choices=GAMES, default=KLABBERJASS, max_length=12, null=False)

    @staticmethod
    def get_series_for_player(user):
        return Series.objects.filter(players__user=user, completed=False).order_by("created")

    @staticmethod
    def get_available_series():
        return Series.objects.filter(completed=False).order_by("created")

    @staticmethod
    def create_series(user, position=1):
        series = Series.objects.create()
        series.add_player(user, position)

    @staticmethod
    def get_by_id(id):
        return Series.objects.get(id=id)

    def get_users_in_series(self):
        series_players = list(SeriesPlayer.objects.filter(series=self).order_by("position"))
        users = [series_player.user for series_player in series_players]
        return users

    def player_in_series(self, user):
        ''' Returns true if player is in series'''
        return len(list(SeriesPlayer.objects.filter(user=user, series=self)))>0

    def add_next_user(self, user):
        num_players = len(SeriesPlayer.objects.filter(series=self))
        self.add_player(user, num_players +1)

    def is_full(self):
        num_players = len(SeriesPlayer.objects.filter(series=self))
        return num_players == GameConfig(self.game_type).num_players

    def add_player(self, user, position):
        if position > GameConfig(self.game_type).num_players:
            raise Exception(f"Error: Position {position} must be less than the number of players  {GameConfig(self.game_type).num_players}")
        elif len(SeriesPlayer.objects.filter(series=self, position = position)) > 0:
            raise Exception(f"Error: SeriesPlayer position {position} is already filled for series {len(self.id)}")
        elif len(SeriesPlayer.objects.filter(series=self, user = user)) > 0:
            raise Exception(f"Error: User {user.username} has alredy joined series {len(self.id)}")
        else:
            SeriesPlayer.objects.create(user= user, position= position, series= self)

    def get_current_game(self):
        games = Game.objects.filter(series=self).order_by('number')
        N = len(games)
        if len(games)>0:
            return games[N-1]
        else:
            return None



class SeriesPlayer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    position = models.SmallIntegerField()
    series = models.ForeignKey(Series, related_name="players", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('series', 'position',)

    def __str__(self):
        return self.user.username

class Game(models.Model):
    KLABBERJASS = 'klabberjass'
    GAMES = [(KLABBERJASS, 'Klabberjass')]
    SUITS = [("spade", 'Spade'), ("heart", 'Heart'), ("diamond", 'Diamond'), ("club", 'Club')]

    game_type = models.CharField(choices=GAMES, default=KLABBERJASS, max_length=12)
    completed = models.BooleanField(default=False)
    series = models.ForeignKey(Series,  related_name="games", on_delete=models.CASCADE, null=True)
    trumps = models.CharField(choices=SUITS, max_length=7)
    number = models.SmallIntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_by_id(id):
        return Game.objects.get(id=id)

    @staticmethod
    def create_game_from_series(series_id):
        series = Series.get_by_id(series_id)

        if len(Game.objects.filter(series=series, completed=False))>0:
            return "Series game in progress"
        else:
            game = Game.objects.create()
            game.series = series
            game.game_type = series.game_type
            game.number = len(Game.objects.filter(series=series, completed=True)) + 1
            users = series.get_users_in_series()
            game.begin(users)
            game.save()

    def begin(self, users):
        self._set_players(users)
        self._deal()

    def _set_players(self, users):
        num_players = GameConfig(self.game_type).num_players
        if len(users)!= num_players:
            raise Exception(f"Error: Incorrect number of players: {len(users)} = {num_players}")
        position = 0
        for user in users:
            position += 1
            Player.objects.get_or_create(user=user, game=self, position = position)

    def get_players(self):
        return list(Player.objects.filter(game=self).order_by('position'))

    def get_num_players(self):
        return len(self.get_players())

    def _deal(self):
        config = GameConfig(self.game_type)
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

    def get_current_or_next_trick(self):
        trick = self.get_current_trick()
        if trick.winner:
            trick.closed = True
            trick.save()
            trick = self.get_current_trick()
        return trick

    def get_current_trick(self):
        open_tricks = Trick.objects.filter(game=self, closed = False).order_by('number')
        if len(open_tricks) > 0:
            return open_tricks[0]
        else:
            return None

    def get_previous_trick(self):
        open_tricks = Trick.objects.filter(game=self).exclude(closed=False).order_by('-number')
        if len(open_tricks) > 0:
            return open_tricks[0]
        else:
            return None

    def get_rules(self):
        config = GameConfig(self.game_type)
        return config.rules

    def get_trick_rules(self):
        config = GameConfig(self.game_type)
        return config.trick



class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.SmallIntegerField()
    game = models.ForeignKey(Game, related_name="players", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('game', 'position', )

    def get_hand(self):
        return list(PlayingCard.objects.filter(game=self.game, player=self))

    def get_username(self):
        return self.user.username


    def get_unplayed_hand(self):
        return list(PlayingCard.objects.filter(game=self.game, player=self, played=False))

    def get_turn(self, trick):
        """Returns a class that checks how the rules of the game apply to the particular hand/trick"""
        rules = self.game.get_rules()
        hand = [card.card for card in self.get_unplayed_hand()]
        trick_cards = [card.card for card in trick.get_playing_cards()]
        trump = self.game.trumps
        return rules(hand, trick_cards, trump)

    def get_legal(self):
        return self.get_turn.legal_cards

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
    game = models.ForeignKey(Game, related_name="tricks", on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, null = True)
    number = models.SmallIntegerField()
    closed = models.BooleanField(default=False, null = False)

    @staticmethod
    def get_by_id(id):
        return Trick.objects.get(id=id)

    def to_play(self):
        lead_position = self.lead().position
        num_cards_in_trick = len(self.get_playing_cards())
        position = self.mod_num_player(lead_position + num_cards_in_trick)
        return Player.objects.get(game = self.game, position = position)

    def mod_num_player(self, number):
        num_players = self.game.get_num_players()
        if number > num_players:
            number = number - num_players
        return number

    def get_playing_cards(self):
        return list(PlayingCard.objects.filter(trick=self).order_by('order_in_trick'))

    def num_cards_played(self):
        return len(self.get_playing_cards())

    def lead(self):
        if self.number == 1:
            # TODO: currently set up that player 1 leads. This could be done differently.
            return Player.objects.get(game=self.game, position = 1)
        else:
            previous_trick = Trick.objects.get(game=self.game, number = self.number -1)
            return previous_trick.winner

    def set_winner_or_pass(self):
        if self.num_cards_played() == self.game.get_num_players():
            self.set_winner()

    def close_or_pass(self):
        if self.winner:
            self.closed = False
            self.save()

    def set_winner(self):
        # TODO: Get Card Look up to use as_number automatically.
        trick_rules = self.game.get_trick_rules()
        trick_cards = [card.card for card in self.get_playing_cards()]
        trick_rules = trick_rules(trick_cards, self.game.trumps)
        winning_card = trick_rules.get_winner()
        self.winner = PlayingCard.objects.get(card=winning_card.as_number(), trick=self).player
        self.save()

class PlayingCard(models.Model):
    card = CardField()
    played = models.BooleanField(default=False)
    game = models.ForeignKey(Game, related_name="cards", on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    trick = models.ForeignKey(Trick, related_name="cards", on_delete=models.SET_NULL, null=True)
    order_in_trick = models.SmallIntegerField(null=True)

    class Meta:
        unique_together = ('card', 'game',)

    @staticmethod
    def get_by_game_and_card(game, card):
        return PlayingCard.objects.get(game=game, card=card)


    def play(self, trick):
        valid, message = self.valid_play(trick)
        if valid:
            self.trick = trick
            self.order_in_trick = trick.num_cards_played() + 1
            self.played = True
            self.save()
            trick.set_winner_or_pass()
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

        return self._validate_play(trick)


    def _validate_game(self, trick):
        return self.game == trick.game

    def _not_played(self):
        return (not self.played)

    def _validate_turn(self, trick):
        return self.player == trick.to_play()

    def _validate_play(self, trick):
        turn = self.player.get_turn(trick)
        return turn.validate_play(self.card)


class Bid(models.Model):
    SUITS = [("spade", 'Spade'), ("heart", 'Heart'), ("diamond", 'Diamond'), ("club", 'Club')]
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    play = models.BooleanField()
    suit = models.CharField(choices=SUITS, max_length=7)




