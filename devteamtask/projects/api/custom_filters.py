from django_filters import rest_framework as filters
from devteamtask.projects.models import Project


class ProjectFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="onwer", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="onwer", lookup_expr='lte')

    class Meta:
        model = Project
        fields = ['category', 'in_stock']
