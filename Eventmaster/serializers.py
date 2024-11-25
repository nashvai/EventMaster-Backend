from rest_framework import serializers
from .models import Event,SubEvent,Component
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.contrib.auth.models import Group

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'

class SubEventSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True, read_only=True)
    class Meta:
        model = SubEvent
        fields = ['id', 'title', 'date', 'description', 'event', 'components']    

class EventSerializer(serializers.ModelSerializer):
    sub_events = SubEventSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'description', 'sub_events']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        # Assign the role based on input (e.g. 'admin' or 'organizer')
        role = validated_data.get('role', 'Event Organizer')
        group = Group.objects.get(name=role)
        user.groups.add(group)
        return user