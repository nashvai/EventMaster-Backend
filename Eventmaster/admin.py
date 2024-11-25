from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

# Register the custom user model
admin.site.register(CustomUser, CustomUserAdmin)

# Create default groups for user types (Event Organizers, Admin)
# You can also set these groups in the admin dashboard directly.

Group.objects.get_or_create(name='Event Organizer')
Group.objects.get_or_create(name='Admin')
