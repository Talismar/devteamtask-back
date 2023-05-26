from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Tag
from devteamtask.core.models import Notification, Tasks


@receiver(post_save, sender=Tag)
def create_notifications(sender, instance: Tag, created: bool, **kwargs):
    pass
