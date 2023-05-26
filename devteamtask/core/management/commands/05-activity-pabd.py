from django.core.management.base import BaseCommand
from devteamtask.projects import models as projects_models
from devteamtask.core import models as core_models
from devteamtask.users.models import User
from random import randint
from faker import Faker

fake = Faker()

AMOUNT_USERS = 30000
AMOUNT_PROJECTS = 1000
AMOUNT_TAGS = 20000
AMOUNT_STATUS = 10000
AMOUNT_TASKS = 1000
AMOUNT_SPRINT = 1000
AMOUNT_NOTIFICATIONS = 10000


def create_users():

    def get_email(username):
        email = username + '@' + fake.email().split("@")[1]
        return email

    for _ in range(AMOUNT_USERS):

        while True:

            user_name = fake.user_name()

            data = {
                "username": user_name,
                "email": get_email(user_name),
                "phone_number": fake.phone_number(),
                "is_superuser": False,
                "is_staff": True,
                "is_active": True,
            }

            if User.objects.filter(username=user_name).exists():
                # print("User %s already exists" % user_name)
                continue
            else:
                User.objects.create(**data)
                break


def create_tags():
    for i in range(AMOUNT_TAGS):
        projects_models.Tag.objects.create(name=fake.swift(length=8))


def create_status():
    for i in range(AMOUNT_STATUS):
        projects_models.Status.objects.create(name=fake.swift(length=8))


def create_projects():
    for _ in range(AMOUNT_PROJECTS):
        leader_id = User.objects.get(pk=randint(1, AMOUNT_USERS))
        product_owner_id = User.objects.get(pk=randint(1, AMOUNT_USERS))

        collaborator_ids = []
        tag_ids = []
        status_ids = []

        for i in range(3):
            collaborator = User.objects.get(pk=randint(1, AMOUNT_USERS))
            tag = projects_models.Tag.objects.get(pk=randint(1, AMOUNT_TAGS))
            status = projects_models.Status.objects.get(pk=randint(1, AMOUNT_STATUS))

            collaborator_ids.append(collaborator)
            tag_ids.append(tag)
            status_ids.append(status)

        data = {
            "name": fake.company(),
            "end_data": "2025-11-01",
            "leader": leader_id,
            "product_owner": product_owner_id,
        }

        instance = projects_models.Project.objects.create(**data)

        instance.collaborators.set(collaborator_ids)
        instance.tags.set(tag_ids)
        instance.status.set(status_ids)

        instance.save()


def create_notification():
    for i in range(AMOUNT_NOTIFICATIONS):
        user = User.objects.get(pk=randint(1, AMOUNT_USERS))

        data = {
            "user": user,
            "title": fake.swift(length=8),
            "description": fake.text()[:46]
        }

        core_models.Notification.objects.create(**data)


def create_sprint():
    for i in range(AMOUNT_SPRINT):
        project = projects_models.Project.objects.get(id=randint(1, AMOUNT_PROJECTS))

        data = {
            "name": fake.swift(length=8),
            "description": fake.text(),
            "state": "1",
            "project_id": project
        }

        core_models.Sprint.objects.create(**data)


def create_tasks():
    for i in range(AMOUNT_TASKS):
        tag = projects_models.Tag.objects.get(id=randint(1, AMOUNT_TAGS))
        status = projects_models.Status.objects.get(id=randint(1, AMOUNT_STATUS))
        assigned_to = User.objects.get(id=randint(1, AMOUNT_USERS))
        created_by = User.objects.get(id=randint(1, AMOUNT_USERS))
        project = projects_models.Project.objects.get(id=randint(1, AMOUNT_PROJECTS))
        sprint = core_models.Sprint.objects.get(id=randint(1, AMOUNT_SPRINT))

        data = {
            "name": "Task " + str(i),
            "description": fake.text()[:80],
            "tag": tag,
            "status": status,
            "priority": randint(1, 3),
            "assigned_to": assigned_to,
            "created_by": created_by,
            "project_id": project,
            "sprint_id": sprint
        }

        core_models.Tasks.objects.create(**data)


class Command(BaseCommand):
    help = "Load default data"

    def handle(self, *args, **options):
        functions = [create_tags, create_status, create_users, create_projects,
                     create_sprint, create_notification, create_tasks]
        models = [
            projects_models.Tag,
            projects_models.Status,
            User,
            projects_models.Project,
            core_models.Sprint,
            core_models.Notification,
            core_models.Tasks
        ]
        names_ = ['TAGS', 'STATUS', 'USERS', 'PROJECTS', 'SPRINT', 'NOTIFICATIONS', 'TASKS']
        AMOUNTS = [AMOUNT_TAGS, AMOUNT_STATUS, AMOUNT_USERS, AMOUNT_PROJECTS,
                   AMOUNT_SPRINT, AMOUNT_NOTIFICATIONS, AMOUNT_TASKS]

        for func, model, name, AMOUNT in zip(functions, models, names_, AMOUNTS):
            if not (model.objects.all().count() >= AMOUNT):
                self.stdout.write(self.style.SUCCESS("CREATE " + name))
                func()
                self.stdout.write(self.style.SUCCESS(name + " CREATED"))
