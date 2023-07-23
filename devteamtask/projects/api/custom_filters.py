from django_filters import rest_framework as filters
from devteamtask.projects.models import Project, EventNotes
from devteamtask.core.models import Tasks


# class ProjectFilter(filters.FilterSet):
#     min_price = filters.NumberFilter(field_name="owner", lookup_expr='gte')
#     max_price = filters.NumberFilter(field_name="owner", lookup_expr='lte')

#     class Meta:
#         model = Project
#         fields = ['category', 'in_stock']


class EventNotesFilter(filters.FilterSet):
    class Meta:
        model = EventNotes
        fields = ["project__id"]


class ProjectTaskFilter(filters.FilterSet):
    tasks_name = filters.CharFilter(field_name="tasks_set__name")

    class Meta:
        model = Project
        fields = ["tasks_name"]
