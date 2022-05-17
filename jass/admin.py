from django.contrib import admin
from jass.models import Series
from jass.models import Series, Game, Trick, PlayingCard


# Register your models here.

class SeriesAdmin(admin.ModelAdmin):
    pass

class GameAdmin(admin.ModelAdmin):
    pass

class TrickAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "winner", "number", "closed")

class PlayingCardAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "player", "played", "trick", "card", "order_in_trick")

admin.site.register(Series, SeriesAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Trick, TrickAdmin)
admin.site.register(PlayingCard, PlayingCardAdmin)