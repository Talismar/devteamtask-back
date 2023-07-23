from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from devteamtask.core.models import Notification, Tasks


def create_notification(user, title: str, description: str | None):
    Notification.objects.create(user=user, title=title, description=description or "")


@receiver(post_save, sender=Tasks)
def on_save(sender, instance: Tasks, created: bool, **kwargs):
    if instance.assigned_to and created:
        create_notification(instance.assigned_to, f"New Task * {instance.name}", instance.description)


@receiver(pre_save, sender=Tasks)
def on_change(sender, instance: Tasks, **kwargs):
    if instance.id is None:  # new object will be created
        pass
    else:
        previous = Tasks.objects.get(id=instance.id)
        # previous.status, instance.status

        if previous.assigned_to is None and instance.assigned_to is not None:
            create_notification(instance.assigned_to, f"New Task * {instance.name}", instance.description)

        if (
            previous.assigned_to is not None
            and instance.assigned_to is not None
            and instance.assigned_to != previous.assigned_to
        ):
            print("Change assigned to")
            create_notification(
                previous.assigned_to,
                "Assignment change",
                f"Task {previous.name} that was assigned to you has been changed to {instance.assigned_to.name}",
            )

            create_notification(instance.assigned_to, f"New Task * {instance.name}", instance.description)
