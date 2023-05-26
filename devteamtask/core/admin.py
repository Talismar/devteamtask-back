from django.contrib import admin

from devteamtask.core.models import (
    Sprint,
    Tasks,
    Notification
)

model_list = [Sprint, Tasks, Notification]

for model in model_list:
    admin.site.register(model)
