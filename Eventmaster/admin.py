from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser,Event,SubEvent,Component

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

# Register the custom user model
admin.site.register(CustomUser, CustomUserAdmin)

# Create default groups for user types (Event Organizers, Admin)
# You can also set these groups in the admin dashboard directly.

Group.objects.get_or_create(name='Event Organizer')
Group.objects.get_or_create(name='Admin')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'description')  # Fields to display in the list view
    search_fields = ('name',)  # Enable search by event name
    list_filter = ('date',)  # Allow filtering by date

@admin.register(SubEvent)
class SubEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'event')  # Fields to display in the list view
    search_fields = ('title', 'event__name')  # Enable search by sub-event title and associated event name
    list_filter = ('date',)  # Allow filtering by date

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'quantity', 'sub_event')  # Fields to display in the list view
    search_fields = ('name', 'sub_event__title')  # Enable search by component name and associated sub-event title
    list_filter = ('type',)  # Allow filtering by type of component