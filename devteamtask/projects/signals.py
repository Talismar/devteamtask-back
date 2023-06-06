from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Tag, EventNotes, Daily
from devteamtask.core.models import Notification, Tasks


@receiver(post_save, sender=Tag)
def create_notifications(sender, instance: Tag, created: bool, **kwargs):
    pass


@receiver(post_save, sender=Project)
def create_event_notes(sender, instance: Project, created: bool, **kwargs):
    if created:
        new_event_notes = EventNotes.objects.create()
        instance.event_notes = new_event_notes
        instance.save()

