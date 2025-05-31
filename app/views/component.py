from typing import Tuple

from django.db.models import ExpressionWrapper, F, IntegerField, Case as _Case, When, Value, CharField
from django.utils.translation import gettext as _
from django.views.generic import ListView

from app.models import Case, CaseFan, GraphicsCard, Memory, Motherboard, PowerSupply, Processor, ProcessorCooler, \
    Storage

Columns = Tuple[Tuple[str, str], ...]
BASE_COLUMNS: Columns = (('id', ''), ('manufacturer__name', 'Manufacturer'), ('model', 'Model'))


class BaseComponentListView(ListView):
    template_name = 'pickpcparts/component/list.html'
    columns = BASE_COLUMNS

    @property
    def raw_columns(self):
        ret = tuple(col[0] for col in self.columns)
        return ret

    def localized_columns(self):
        ret = tuple(_(col[1]) for col in self.columns)
        return ret

    def get_queryset(self):
        return self.model.objects.order_by('manufacturer').values(*self.raw_columns)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = {item.pop('id'): item for item in context['object_list']}
        context.update({
            'columns': self.localized_columns()[1:],  # remove id column from UI
            'rows': rows,
        })
        return context


class CaseListView(BaseComponentListView):
    model = Case
    columns = (
        *BASE_COLUMNS,
        ('formfactor__name', 'Form Factor'),
        ('external_volume', 'External Volume'),
    )


class CaseFanListView(BaseComponentListView):
    model = CaseFan
    columns = (
        *BASE_COLUMNS,
        ('size', 'Size'),
        ('rpm', 'RPM'),
        ('noise_level', 'Noise Level (db)'),
        ('pwm', 'PWM'),
    )


class GraphicsCardListView(BaseComponentListView):
    model = GraphicsCard
    columns = (
        *BASE_COLUMNS,
        ('memory', 'Memory (GB)'),
        ('core_clock', 'Core Clock (MHz)'),
        ('boost_clock', 'Boost Clock (MHz)'),
        ('length', 'Length (cm)'),
    )


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


class MotherboardListView(BaseComponentListView):
    model = Motherboard
    columns = (
        *BASE_COLUMNS,
        ('max_memory', 'Max Memory (GB)'),
        ('memory_slots', 'Memory Slots'),
        ('supported_memory__name', 'Supported Memory'),
        ('formfactor__name', 'Form Factor'),
        ('socket__name', 'Socket'),
    )


class PowerSupplyListView(BaseComponentListView):
    model = PowerSupply
    columns = (
        *BASE_COLUMNS,
        ('formfactor__name', 'Form Factor'),
        ('wattage', 'Wattage'),
        ('efficiency_label', 'Efficiency'),
        ('modularity_label', 'Modularity'),
    )

    def get_queryset(self):
        # noinspection PyTypeChecker
        return self.model.objects.annotate(
            efficiency_label=_Case(
                *[When(efficiency=choice.value, then=Value(choice.label))
                  for choice in PowerSupply.Efficiency],
                default=Value('Unknown'),
                output_field=CharField()
            ),
            modularity_label=_Case(
                *[When(modularity=choice.value, then=Value(choice.label))
                  for choice in PowerSupply.Modularity],
                default=Value('Unknown'),
                output_field=CharField()
            )
        ).order_by('manufacturer').values(*self.raw_columns)


class ProcessorListView(BaseComponentListView):
    model = Processor
    columns = (
        *BASE_COLUMNS,
        ('core_count', 'Core Count'),
        ('core_clock', 'Core Clock (MHz)'),
        ('boost_clock', 'Boost Clock (MHz)'),
        ('tdp', 'TDP (W)'),
        ('socket__name', 'Socket'),
    )


class ProcessorCoolerListView(BaseComponentListView):
    model = ProcessorCooler
    columns = (
        *BASE_COLUMNS,
        ('rpm', 'RPM'),
        ('noise_level', 'Noise Level (db)'),
        ('size', 'Size (cm)'),
        ('socket__name', 'Socket'),
    )


class StorageListView(BaseComponentListView):
    model = Storage
    columns = (
        *BASE_COLUMNS,
        ('capacity', 'Capacity (GB)'),
        ('cache', 'Cache (MB)'),
        ('form_factor__name', 'Form Factor'),
        ('interface__name', 'Interface'),
    )
