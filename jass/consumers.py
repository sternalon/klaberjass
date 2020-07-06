import re
import logging
# from channels import Group
# from channels.sessions import channel_session
# from .models import Game, GameSquare
# from channels.auth import channel_session_user
from channels.generic.websocket import JsonWebsocketConsumer

log = logging.getLogger(__name__)


class LobbyConsumer(JsonWebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["lobby"]

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        self.message.reply_channel.send({"accept": True})
        pass

    def receive(self, content, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        http_user = True

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass