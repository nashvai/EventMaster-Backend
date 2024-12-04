from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsEventOrganizer,IsAdminUser,IsUnregisteredUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Event, SubEvent, Component,CustomUser
from .serializers import EventSerializer, SubEventSerializer, ComponentSerializer, UserSerializer

User = get_user_model()  # Get the custom user model

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsUnregisteredUser]  # Restrict access to authenticated users
    
    def perform_create(self, serializer):
        # Set the created_by field to the current user
        serializer.save(created_by=self.request.user)

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
        # For non-admin users, use created_by filter
        queryset = Event.objects.filter(created_by=self.request.user)
        
        # Fall back to a default user if no created_by is set (for pre-existing events)
        if not queryset.exists():
            default_user = User.objects.get(username='AdminNa')  # Or assign any other user
            queryset = Event.objects.filter(created_by=default_user)
        
        return queryset
    
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsUnregisteredUser]
    
    def perform_create(self, serializer):
        # Set the created_by field to the current user
        serializer.save(created_by=self.request.user)

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
        # Get the event ID from the URL
        event_id = self.kwargs.get('event_pk')  # Ensure this matches your URL routing
        
        # Fetch the sub-events related to the specified event
        queryset = SubEvent.objects.filter(event_id=event_id)

        # If the user is an admin, return all sub-events for the specified event
        if self.request.user.role == 'admin':
            return queryset  # Admin can access all sub-events

        # For organizers, filter by created_by
        return queryset.filter(created_by=self.request.user)
      
      

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
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        # Set the created_by field to the current user
        serializer.save(created_by=self.request.user)
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
        # Admins can access all components
        if self.request.user.role == 'admin':
            return Component.objects.all()
        
        # For organizers, filter components by their sub-events
        queryset = Component.objects.filter(sub_event__event__created_by=self.request.user)

        # Fall back to a default user if no created_by is set (for pre-existing components)
        if not queryset.exists():
            default_user = User.objects.get(username='AdminNa')  # Replace with actual default user if necessary
            queryset = Component.objects.filter(sub_event__event__created_by=default_user)

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
         # Default role assignment if not provided
            if not user.role:
              user.role = 'organizer'  # Default role
              user.save()
            # The group assignment is handled by the serializer's create method
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)