from django.contrib import admin

from devteamtask.projects.models import (
    Project,
    Invite,
    Tag,
    Status,
    Sprint,
)

model_list = [Project, Invite, Tag, Status, Sprint]

for model in model_list:
    admin.site.register(model)
