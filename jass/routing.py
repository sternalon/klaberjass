from jass.consumers import LobbyConsumer, SeriesConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'lobby/$', LobbyConsumer),
    re_path(r'series/(?P<series_id>\d+)/$', SeriesConsumer),

]
