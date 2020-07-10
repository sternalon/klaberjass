from django.contrib import admin
from jass.models import Series


# Register your models here.

class SeriesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Series, SeriesAdmin)