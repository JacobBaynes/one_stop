from rest_framework import serializers
from .models import Person
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'email', 'groups')


class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Person
        fields = (
            'user', 'uuid', 'sys_ID', 'mname', 'classification', 'campusroom'
        )
