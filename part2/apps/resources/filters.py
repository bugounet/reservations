import django_filters

from .models import Resource


class ResourceFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(
        field_name='type', lookup_expr='istartswith'
    )
    location = django_filters.CharFilter(
        field_name='location', lookup_expr='icontains'
    )

    class Meta:
        model = Resource
        fields = ['type', 'location']
