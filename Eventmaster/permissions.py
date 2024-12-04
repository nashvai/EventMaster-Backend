from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsEventOrganizer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'organizer'

    def has_object_permission(self, request, view, obj):
        # Ensure the organizer is accessing their own event
        return obj.created_by == request.user

class IsUnregisteredUser(BasePermission):
    def has_permission(self, request, view):
        # Allow access only if the user is not authenticated
        return not request.user.is_authenticated
