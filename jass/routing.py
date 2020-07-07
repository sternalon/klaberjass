from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from jass.consumers import LobbyConsumer
# from channels.routing import route, route_class
# from channels.staticfiles import StaticFilesConsumer
# from game import consumers

application = ProtocolTypeRouter({

    # WebSocket  handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^lobby/$", LobbyConsumer),
        ])
    ),


})

#
# # routes defined for channel calls
# # this is similar to the Django urls, but specifically for Channels
# channel_routing = [
#     route_class(consumers.LobbyConsumer,  path=r"^/lobby/"),
# ]