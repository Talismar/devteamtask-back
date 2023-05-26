from django.db.models.signals import post_save
from django.dispatch import receiver
from devteamtask.core.models import Notification, Tasks


@receiver(post_save, sender=Tasks)
def create_notifications(sender, instance: Tasks, created: bool, **kwargs):
    data: dict = {}

    if instance.assigned_to and created:
        data["user"] = instance.assigned_to
        data["title"] = instance.name
        data["description"] = instance.description

        Notification.objects.create(**data)

    # TODO: make logic for when task to update
    # remove current user and create new
