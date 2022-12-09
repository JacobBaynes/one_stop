"""purple_pages URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from api import views as api_v
from persons import views
from django.conf import settings
from django.conf.urls.static import static
#from persons.views import student_home_view

router = routers.DefaultRouter()
router.register(r'users', api_v.UserViewSet)
router.register(r'groups', api_v.GroupViewSet)
router.register(r'persons', views.PersonViewSet)


urlpatterns = [
    #### Django specific urls####
    path('admin/', admin.site.urls),
    # This path leads to the django.contrib.auth package which contains urls for login and logout
    path('', include("django.contrib.auth.urls")),

    #### Project specific urls####
    path('api/', include(router.urls)),
    path('persons/', include('persons.urls')),
    path('dining/', include('dining.urls')),
]
