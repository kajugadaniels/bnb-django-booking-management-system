from home.models import *
from django.contrib import admin

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)