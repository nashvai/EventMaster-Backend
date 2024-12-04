from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='events_created', on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.name
    
class SubEvent(models.Model):
    event = models.ForeignKey(Event, related_name='sub_events', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subevents_created', on_delete=models.CASCADE,default=1)


    def __str__(self):
        return self.title

class Component(models.Model):
    sub_event = models.ForeignKey(SubEvent, related_name="components", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)  # For categorizing, e.g., seating, AV, catering
    quantity = models.IntegerField()  # Quantity of items or units for this component
    notes = models.TextField(blank=True, null=True)  # Optional additional details
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='components_created', 
        on_delete=models.CASCADE,
        default=1  # Use the ID of an existing user, for example, ID 1 for admin
    )

    def __str__(self):
        return f"{self.name} ({self.type})"

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('unregistered', 'Unregistered'),
        ('organizer', 'Event Organizer'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='organizer')

    # Add related_name to avoid clashes with the default User model's groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # This is the related_name for the CustomUser's groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # This is the related_name for the CustomUser's user_permissions
        blank=True
    )

    def __str__(self):
        return self.username