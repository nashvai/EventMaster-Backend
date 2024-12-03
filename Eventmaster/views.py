from rest_framework.permissions import IsAuthenticated, AllowAny
#from .permissions import IsOrganizerOrAdmin 
#from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Event, SubEvent, Component,CustomUser
from .serializers import EventSerializer, SubEventSerializer, ComponentSerializer, UserSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated,IsOrganizerOrAdmin]  # Restrict access to authenticated users

    def update(self, request, *args, **kwargs):
        required_fields = ['name', 'date', 'description']
        missing_fields = [field for field in required_fields if field not in request.data]
        
        if missing_fields:
            return Response(
                {"error": f"Missing fields: {', '.join(missing_fields)}"},
                status=420
            )


        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SubEventViewSet(viewsets.ModelViewSet):
    queryset = SubEvent.objects.all()
    serializer_class = SubEventSerializer
    #authentication_classes = [JWTAuthentication]


    def get_queryset(self):
        event_id = self.kwargs.get('event_pk')  # Use 'event_pk' to match the nested router
        if event_id:
            return SubEvent.objects.filter(event_id=event_id)
        

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
    #authentication_classes = [JWTAuthentication]
    

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

class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        # Get the role from the request data, default to 'Event Organizer'
        role = request.data.get('role', 'organizer')  # Default is 'organizer' if not specified
        
        if role not in dict(CustomUser.ROLE_CHOICES).keys():
            return Response({"error": "Invalid role specified."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['role'] = role
          # Make sure to validate the data using the serializer
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            return super().create(request, *args, **kwargs)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)