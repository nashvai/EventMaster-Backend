from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Event, SubEvent, Component
from .serializers import EventSerializer, SubEventSerializer, ComponentSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def update(self, request, *args, **kwargs):
        required_fields = ['name', 'date', 'description']
        missing_fields = [field for field in required_fields if field not in request.data]
        
        if missing_fields:
            return Response(
                {"error": f"Missing fields: {', '.join(missing_fields)}"},
                status=422
            )


        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SubEventViewSet(viewsets.ModelViewSet):
    queryset = SubEvent.objects.all()
    serializer_class = SubEventSerializer

    def get_queryset(self):
        event_id = self.kwargs.get('event')
        print(f"Looking for sub-events for event_id: {event_id}")
        if event_id:
            return SubEvent.objects.filter(event_id=event_id)
        else:
            return SubEvent.objects.all()

    def update(self, request, *args, **kwargs):
        required_fields = ['title', 'date', 'description', 'event']
        missing_fields = [field for field in required_fields if field not in request.data]
        
        if missing_fields:
            return Response(
                {"error": f"Missing fields: {', '.join(missing_fields)}"},
                status=420
            )


        # Check if the event exists
        event_id = request.data.get('event')
        if event_id and not Event.objects.filter(id=event_id).exists():
            return Response(
                {"error": f"Event with ID {event_id} does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

    def get_queryset(self):
        sub_event_id = self.kwargs['sub_event_pk']
        return Component.objects.filter(sub_event_id=sub_event_id)

    def update(self, request, *args, **kwargs):
        required_fields = ['name', 'type', 'quantity', 'notes', 'sub_event']
        missing_fields = [field for field in required_fields if field not in request.data]
        
        if missing_fields:
            return Response(
                {"error": f"Missing fields: {', '.join(missing_fields)}"},
                status=420
            )


        # Check if the sub_event exists
        sub_event_id = request.data.get('sub_event')
        if sub_event_id and not SubEvent.objects.filter(id=sub_event_id).exists():
            return Response(
                {"error": f"SubEvent with ID {sub_event_id} does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
