from django.contrib import admin

from devteamtask.core.models import (
    Sprint,
    Tasks
)

model_list = [Sprint, Tasks]

for model in model_list:
    admin.site.register(model)
