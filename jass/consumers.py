import re
import logging
# from channels import Group
# from channels.sessions import channel_session
from .models import Series, Game
# from channels.auth import channel_session_user
from channels.generic.websocket import JsonWebsocketConsumer
from channels import layers
from asgiref.sync import async_to_sync
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
    print("AAAAAAA")

    # def connection_groups(self, **kwargs):
    #     """
    #     Called to return the list of groups to automatically add/remove
    #     this connection to/from.
    #     """
    #     # this sets the game group name, so we can communicate directly with
    #     # those channels in the game
    #     return ["series-{0}".format(kwargs['series_id'])]
    #
    # def connect(self, message, **kwargs):
    #     """
    #     Perform things on connection start
    #     """
    #     self.message.reply_channel.send({"accept": True})
    #     pass

    def receive(self, content, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        # include the Django user in the request
        channel_session_user = True
        action = content['action']

        # handle based on the specific action called
        if action == 'claim_square':
            # get the square object
            square = GameSquare.get_by_id(content['square_id'])
            # claim it for the user
            square.claim('Selected', self.message.user)

        if action == 'chat_text_entered':
            # chat text
            game = Game.get_by_id(content['game_id'])
            game.add_log(content['text'], self.message.user)
            game.send_game_update()

        if action == 'create_game':
            print("YOYLYOYOYOYOOYOYOY")
            # game = Game.create_game_from_series(content['series_id'])


    # def disconnect(self, message, **kwargs):
    #     """
    #     Perform things on connection close
    #     """

