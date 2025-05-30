from django.db.models import ExpressionWrapper, F, IntegerField

from app.models import Memory
from .base import BaseComponentListView, BASE_COLUMNS


class MemoryListView(BaseComponentListView):
    model = Memory

    columns = (
        *BASE_COLUMNS,
        ('total_capacity', 'Total Capacity (GB)'),
        ('modules', 'Modules'),
        ('speed', 'Speed (MT/s)'),
        ('first_word_latency', 'First Word Latency (ns)'),
        ('cas_latency', 'CAS Latency (ns)'),
        ('type__name', 'Type'),
    )

    def get_queryset(self):
        return self.model.objects.annotate(
            total_capacity=ExpressionWrapper(
                F('capacity_per_module') * F('modules'),
                output_field=IntegerField()),
        ).order_by('manufacturer').values(*self.raw_columns)
