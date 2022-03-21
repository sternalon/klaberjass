from django.contrib import admin
from jass.models import Series
from jass.models import Series, Game


# Register your models here.

class SeriesAdmin(admin.ModelAdmin):
    pass

class GameAdmin(admin.ModelAdmin):
    pass

admin.site.register(Series, SeriesAdmin)
admin.site.register(Game, GameAdmin)