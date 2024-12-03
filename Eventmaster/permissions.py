from rest_framework.permissions import BasePermission

class IsOrganizerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is either an Organizer or Admin
        return request.user.role in ['organizer', 'admin']
