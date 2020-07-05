from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from jass.consumers import LobbyConsumer


application = ProtocolTypeRouter({

    # WebSocket  handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^jass/lobby/$", LobbyConsumer),
        ])
    ),


})
