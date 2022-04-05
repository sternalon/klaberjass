from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# from game.models import *
import json
import time
# from channels import Group
from .serializers import *
from .models import Series, SeriesPlayer


def send_available_series_update():
    """
    Send the updated series information to the lobby channel group
    """
    avail_series_list = Series.get_available_series()
    avail_serializer = SeriesSerializer(avail_series_list, many=True)

    layer = get_channel_layer()
    async_to_sync(layer.group_send)('lobby', {"type": "lobby.send", 'text': json.dumps(avail_serializer.data)})


@receiver(post_save, sender=Series)
def new_series_handler(**kwargs):
    """
    When a new series is created, this builds a list of all open series and
    sends it down to all channels in the 'lobby' group
    """
    # if new
    if kwargs['created']:
        send_available_series_update()

@receiver(post_save, sender=SeriesPlayer)
def new_series_handler(**kwargs):
    """
    When a new series player is created, this builds a list of all open series and
    sends it down to all channels in the 'lobby' group.
    This is needed because a Series is created before the players are created.
    """
    # if new
    if kwargs['created']:
        send_available_series_update()