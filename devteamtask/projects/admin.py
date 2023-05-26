from django.contrib import admin

from devteamtask.projects.models import (
    Project,
    Invite,
    Tag,
    Status,
    EventNotes,
    Daily
)

model_list = [Project, Invite, Tag, Status, EventNotes, Daily]

for model in model_list:
    admin.site.register(model)
