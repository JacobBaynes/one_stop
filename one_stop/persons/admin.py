from django.contrib import admin
from .models import Person
from django.contrib.auth.models import User


class PersonAdmin(admin.ModelAdmin):
    fields = ["uuid", "user", "classification", "position", "mname",
              "preferred_name", "dob", "phone", "campusroom"]
    search_fields = ("uuid", "user__username", "mname", "preferred_name")
    list_display = ("uuid", "user", "classification", "position", "mname",
                    "preferred_name", "phone", "campusroom")


admin.site.register(Person, PersonAdmin)
