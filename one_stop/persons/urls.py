from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# app_name = 'persons'
urlpatterns = [
    path('', views.user_detail, name='user-detail'),
    path('user_detail/', views.user_detail, name='user-detail'),
    path('user_detail/<int:sys_ID>/', views.user_detail, name='user-detail'),
    path('directory/', views.directory, name='directory'),
    path('test/', views.test),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
