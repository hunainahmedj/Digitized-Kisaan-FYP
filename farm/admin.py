from django.contrib import admin

from .models import Farm, Picture, Coordinates, Country

admin.site.register(Farm)
admin.site.register(Picture)
admin.site.register(Coordinates)
admin.site.register(Country)
