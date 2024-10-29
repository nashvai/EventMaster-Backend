from rest_framework import serializers
from .models import Event,SubEvent,Component

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

