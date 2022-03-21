from django.contrib.auth.models import User
from .models import Game, Series, SeriesPlayer, PlayingCard, Trick, Player
from rest_framework import serializers
from .utils import Card

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


class PlayingCardSerializer(serializers.ModelSerializer):
    suit = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()

    def get_suit(self, obj):
        card = Card.number_to_card(obj.id)
        return card.suit if card else None

    def get_number(self, obj):
        card = Card.number_to_card(obj.id)
        return card.number if card else None

    class Meta:
        model = PlayingCard
        fields = ('id', 'suit', 'number', 'player', 'game', 'trick', 'order_in_trick', 'played')


class PlayerSerializer(serializers.ModelSerializer):
    hand = serializers.SerializerMethodField()

    def get_hand(self, obj):
        hand = obj.get_hand()
        hand = [PlayingCardSerializer(card).data for card in hand]
        return hand

    class Meta:
        model = Player
        fields = ('id', 'user', 'position', 'game', 'hand')


class TrickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trick
        fields = ('id', 'game', 'winner', 'number', 'cards')

class GameSerializer(serializers.ModelSerializer):
    cards = PlayingCardSerializer(many=True)
    tricks = TrickSerializer(many=True)
    players = PlayerSerializer(many= True)

    # TODO: Might want to only return the currrent trick is performance is slow
    # current_trick = serializers.SerializerMethodField()

    # def get_current_trick(self,obj):
    #     current_trick = obj.get_current_trick()
    #     return TrickSerializer(current_trick).data

    class Meta:
        model = Game
        fields = ('id', 'number', 'trumps', 'completed', 'cards', 'tricks', 'players')
        depth = 2

class SeriesPlayersSerializer(serializers.ModelSerializer):
    # user_username = serializers.RelatedField(source='username', read_only=True)
    username = serializers.CharField(source='user.username')

    class Meta:
        model = SeriesPlayer
        fields = ('username', 'position')
        depth = 1

class SeriesSerializer(serializers.ModelSerializer):
    players = SeriesPlayersSerializer(many=True)
    # TODO: Might want to only return the current game is performance is slow
    current_game = serializers.SerializerMethodField()

    def get_current_game(self,obj):
        current_game = obj.get_current_game()
        return current_game.id if current_game else None


    class Meta:
        model = Series
        fields = ('id', 'score1', 'score2', 'players', 'completed', 'current_game')
        depth = 1
