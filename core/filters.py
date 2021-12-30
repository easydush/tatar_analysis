import django_filters

from core.models import TriggerNews


class NewsViewFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = TriggerNews
        fields = ['last_update', 'rate']
