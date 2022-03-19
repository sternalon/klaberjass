from django.contrib.auth.models import User
from .models import Game, Series, SeriesPlayer, PlayingCard
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


class PlayingCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayingCard
        fields = ('id', 'player', 'game', 'trick', 'order_in_trick','played')

class GameSerializer(serializers.ModelSerializer):
    cards = PlayingCardSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'number', 'game_type', 'trumps', 'completed', 'cards')
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
    games = GameSerializer(many=True)

    class Meta:
        model = Series
        fields = ('id', 'score1', 'score2', 'game_type', 'players', 'games', 'completed', 'created')
        depth = 1
