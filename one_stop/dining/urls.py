from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LocationListView

urlpatterns = [
    path('', LocationListView.as_view(), name='location-list')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
