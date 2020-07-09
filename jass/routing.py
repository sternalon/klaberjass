from jass.consumers import LobbyConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'lobby/$', LobbyConsumer),
]