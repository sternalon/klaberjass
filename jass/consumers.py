import re
import logging
# from channels import Group
# from channels.sessions import channel_session
from .models import Series, Game, PlayingCard, Trick
# from channels.auth import channel_session_user
from channels.generic.websocket import JsonWebsocketConsumer
from channels import layers
from asgiref.sync import async_to_sync
from .utils import Card
from jass import signals

log = logging.getLogger(__name__)


class LobbyConsumer(JsonWebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True
    groups = ["lobby"]

    # def connection_groups(self, **kwargs):
    #     """
    #     Called to return the list of groups to automatically add/remove
    #     this connection to/from.
    #     """
    #     return ["lobby"]

    # def connect(self, **kwargs):
    #     """
    #     Perform things on connection start - can be removed.
    #     """
    #     self.accept()
    #     # async_to_sync(self.channel_layer.group_add)("lobby", self.channel_name)
    #     pass

    # def receive(self, text_data=None, bytes_data=None):
    def receive_json(self, content=None, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        channel_session_user = True
        http_user = True

        # get the action that's coming in
        action = content['action']
        if action == 'create_series':
            # create a new game using the part of the channel name
            Series.create_series(self.scope["user"])

    def lobby_send(self, event):
        self.send(text_data=event["text"])

    # def disconnect(self, message, **kwargs):
    #     """
    #     Perform things on connection close
    #     """
    #     # async_to_sync(self.channel_layer.group_discard)("lobby", self.channel_name)
    #     pass


class SeriesConsumer(JsonWebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Initializing Series Consumer", self.scope)
        series_id = self.scope["url_route"]["kwargs"]["series_id"]
        group = "series-{0}".format(series_id)
        print("Consumer group set to ", group)
        self.groups = [group]


    def receive_json(self, content=None, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        channel_session_user = True
        http_user = True


        # get the action that's coming in
        action = content['action']
        if action == 'create_game':
            series_id = self.scope["url_route"]["kwargs"]["series_id"]
            # create the next game in the series
            Game.create_game_from_series(series_id)
            series = Series.get_by_id(series_id)

        if action == 'play_card':
            game_id = content['game_id']
            suit = content['suit']
            number = content['number']
            card = Card(number=number , suit = suit)

            game = Game.get_by_id(game_id)
            trick = game.get_current_or_next_trick()
            playing_card = PlayingCard.get_by_game_and_card(game_id, card.card_number)

            valid, message = playing_card.play(trick)
            print("Response from playing card:", valid, message)

            if valid:
                signals.send_game_update(game)


    def series_send(self, event):
        self.send(text_data=event["text"])



    # def disconnect(self, message, **kwargs):
    #     """
    #     Perform things on connection close
    #     """


