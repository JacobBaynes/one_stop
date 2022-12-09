from django.views.generic.list import ListView
from django.shortcuts import render
from django.utils import timezone
from .models import Location

# Create your views here.
class LocationListView(ListView):
    model = Location
    template_name = "location_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
    