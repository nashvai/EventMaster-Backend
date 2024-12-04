from rest_framework import serializers
from .models import Event,SubEvent,Component,CustomUser
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
        # Ensure the role is always 'organizer' for registration
        validated_data['role'] = validated_data.get('role', 'organizer')  # Default to 'organizer'

        # Create the user
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data['role'],  # Set role to 'organizer' or as provided
        )
        
        # Ensure the 'Event Organizer' group exists
        group, created = Group.objects.get_or_create(name='Event Organizer')
        
        # Add the user to the 'Event Organizer' group
        user.groups.add(group)
        
        return user
