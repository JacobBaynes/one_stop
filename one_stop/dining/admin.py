from django.contrib import admin
from .models import Location

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    fields = ["name", "phone_number", "site", "menu", "hours", "image"]
    list_display = ("name", "phone_number", "site", "menu", "hours", "image")


admin.site.register(Location, LocationAdmin)