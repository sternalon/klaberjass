from django.contrib.auth.models import User
from .models import Game, Series
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'completed', 'series', 'trumps', 'created', 'modified')
        depth = 2

class SeriesPlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'user', 'position', 'series')
        depth = 1

class SeriesSerializer(serializers.ModelSerializer):
    players = SeriesPlayersSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = ('id', 'score1', 'score2', 'game_type', 'players', 'completed', 'created')
        depth = 2