from rest_framework import viewsets
from .models import Event,SubEvent,Component
from .serializers import EventSerializer,SubEventSerializer,ComponentSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class SubEventViewSet(viewsets.ModelViewSet):
    queryset = SubEvent.objects.all()
    serializer_class = SubEventSerializer    

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer    