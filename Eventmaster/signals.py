from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    # Automatically create default groups
    Group.objects.get_or_create(name='Event Organizer')
    Group.objects.get_or_create(name='Admin')
