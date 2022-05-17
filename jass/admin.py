from django.contrib import admin
from jass.models import Series
from jass.models import Series, Game, Trick


# Register your models here.

class SeriesAdmin(admin.ModelAdmin):
    pass

class GameAdmin(admin.ModelAdmin):
    pass

class TrickAdmin(admin.ModelAdmin):
    list_display = ("game", "winner", "number", "closed")

admin.site.register(Series, SeriesAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Trick, TrickAdmin)