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
    user = serializers.SerializerMethodField()

    def get_suit(self, obj):
        return obj.card.suit if obj.card else None

    def get_number(self, obj):
        return obj.card.number if obj.card else None

    def get_user(self, obj):
        return obj.player.user.id if obj.player else None

    class Meta:
        model = PlayingCard
        fields = ('id', 'suit', 'number', 'player', 'game', 'trick', 'order_in_trick', 'played', 'user')

class PlayerSerializer(serializers.ModelSerializer):
    hand = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_hand(self, obj):
        hand = obj.get_hand()
        hand = [PlayingCardSerializer(card).data for card in hand]
        return hand

    def get_username(self, obj):
        username = obj.get_username()
        return username

    class Meta:
        model = Player
        fields = ('id', 'user', 'username', 'position', 'game', 'hand')


class TrickSerializer(serializers.ModelSerializer):
    cards = PlayingCardSerializer(many=True)

    class Meta:
        model = Trick
        fields = ('id', 'game', 'winner', 'number', 'cards')

class GameSerializer(serializers.ModelSerializer):
    current_trick = serializers.SerializerMethodField()
    previous_trick = serializers.SerializerMethodField()
    players = PlayerSerializer(many= True)

    # TODO: Might want to only return the current trick is performance is slow

    def get_current_trick(self,obj):
        current_trick = obj.get_current_trick()
        return TrickSerializer(current_trick).data

    def get_previous_trick(self,obj):
        current_trick = obj.get_previous_trick()
        return TrickSerializer(current_trick).data

    class Meta:
        model = Game
        fields = ('id', 'number', 'trumps', 'completed', 'current_trick', 'previous_trick', 'players')
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
    current_game = serializers.SerializerMethodField()

    def get_current_game(self,obj):
        current_game = obj.get_current_game()
        return current_game.id if current_game else None


    class Meta:
        model = Series
        fields = ('id', 'score1', 'score2', 'players', 'completed', 'current_game')
        depth = 1
