from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsEventOrganizer,IsAdminUser,IsUnregisteredUser
#from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.contrib.auth.models import Group
from .models import Event, SubEvent, Component,CustomUser
from .serializers import EventSerializer, SubEventSerializer, ComponentSerializer, UserSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    #authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsUnregisteredUser]  # Restrict access to authenticated users
    def get_permissions(self):
       # If authenticated, check the user's role
        if self.request.user.is_authenticated:
            if self.request.user.role == 'admin':
                return [IsAdminUser()]
            elif self.request.user.role == 'organizer':
                return [IsEventOrganizer()]
        # Return the super permissions (for IsUnregisteredUser and IsAuthenticated)
        return super().get_permissions()

    def get_queryset(self):
        # Admin can access all events; organizers only their own
        if self.request.user.role == 'admin':
            return Event.objects.all()
        return Event.objects.filter(created_by=self.request.user)  # Organizer-specific
    
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
    permission_classes = [IsAuthenticated,IsUnregisteredUser]

    def get_permissions(self):
      # If authenticated, check the user's role
        if self.request.user.is_authenticated:
            if self.request.user.role == 'admin':
                return [IsAdminUser()]
            elif self.request.user.role == 'organizer':
                return [IsEventOrganizer()]
        # Return the super permissions (for IsUnregisteredUser and IsAuthenticated)
        return super().get_permissions()

    def get_queryset(self):
        # Admin can access all sub-events; organizers only within their events
        # Apply role-based filtering
        if self.request.user.role == 'admin':
            queryset = Event.objects.all()
        else:  # Organizer
            queryset = Event.objects.filter(created_by=self.request.user)

        # Add any additional filters (e.g., query params for specific events)
        event_id = self.request.query_params.get('event_pk')
        if event_id:
            queryset = queryset.filter(id=event_id)

        return queryset
        

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
    permission_classes = [IsAuthenticated,IsUnregisteredUser]

    def get_permissions(self):
       # If authenticated, check the user's role
        if self.request.user.is_authenticated:
            if self.request.user.role == 'admin':
                return [IsAdminUser()]
            elif self.request.user.role == 'organizer':
                return [IsEventOrganizer()]
        # Return the super permissions (for IsUnregisteredUser and IsAuthenticated)
        return super().get_permissions()

    def get_queryset(self):
        # Admins can access all components; organizers only their sub-events
        if self.request.user.role == 'admin':
            return Component.objects.all()
        else:  # Organizer
            queryset = Component.objects.filter(sub_event__event__created_by=self.request.user)

        # Additional filters (e.g., by sub-event ID)
        sub_event_id = self.request.query_params.get('sub_event_pk')
        if sub_event_id:
            queryset = queryset.filter(sub_event_id=sub_event_id)

        return queryset

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
        # Use the provided serializer, which now handles default role assignment
        serializer = self.get_serializer(data=request.data)
        
        # Validate and save the new user
        if serializer.is_valid():
            user = serializer.save()

            # The group assignment is handled by the serializer's create method
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)