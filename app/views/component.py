from typing import Tuple

from django.db.models import ExpressionWrapper, F, IntegerField, Case as _Case, When, Value, CharField
from django.utils.translation import gettext as _
from django.views.generic import ListView

from app.models import Case, CaseFan, GraphicsCard, Memory, Motherboard, PowerSupply, Processor, ProcessorCooler, \
    Storage

Columns = Tuple[Tuple[str, str], ...]
BASE_COLUMNS: Columns = (('id', ''), ('manufacturer__name', _('Manufacturer')), ('model', _('Model')))


class BaseComponentListView(ListView):
    template_name = 'pickpcparts/component/list.html'
    columns = BASE_COLUMNS

    @property
    def raw_columns(self):
        ret = tuple(col[0] for col in self.columns)
        return ret

    @property
    def localized_columns(self):
        ret = tuple(col[1] for col in self.columns)
        return ret

    def get_queryset(self):
        return self.model.objects.order_by('manufacturer').values(*self.raw_columns)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = {item.pop('id'): item for item in context['object_list']}
        context.update({
            'columns': self.localized_columns[1:],  # remove id column from UI
            'rows': rows,
        })
        return context


class CaseListView(BaseComponentListView):
    model = Case
    columns = (
        *BASE_COLUMNS,
        ('formfactor__name', _('Form Factor')),
        ('external_volume', _('External Volume')),
    )


class CaseFanListView(BaseComponentListView):
    model = CaseFan
    columns = (
        *BASE_COLUMNS,
        ('size', _('Size')),
        ('rpm', _('RPM')),
        ('noise_level', _('Noise Level (db)')),
        ('pwm', _('PWM')),
    )


class GraphicsCardListView(BaseComponentListView):
    model = GraphicsCard
    columns = (
        *BASE_COLUMNS,
        ('memory', _('Memory (GB)')),
        ('core_clock', _('Core Clock (MHz)')),
        ('boost_clock', _('Boost Clock (MHz)')),
        ('length', _('Length (cm)')),
    )


class MemoryListView(BaseComponentListView):
    model = Memory

    columns = (
        *BASE_COLUMNS,
        ('total_capacity', _('Total Capacity (GB)')),
        ('modules', _('Modules')),
        ('speed', _('Speed (MT/s)')),
        ('first_word_latency', _('First Word Latency (ns)')),
        ('cas_latency', _('CAS Latency (ns)')),
        ('type__name', _('Type')),
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
        ('max_memory', _('Max Memory (GB)')),
        ('memory_slots', _('Memory Slots')),
        ('supported_memory__name', _('Supported Memory')),
        ('formfactor__name', _('Form Factor')),
        ('socket__name', _('Socket')),
    )


class PowerSupplyListView(BaseComponentListView):
    model = PowerSupply
    columns = (
        *BASE_COLUMNS,
        ('formfactor__name', _('Form Factor')),
        ('wattage', _('Wattage')),
        ('efficiency_label', _('Efficiency')),
        ('modularity_label', _('Modularity')),
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
        ('core_count', _('Core Count')),
        ('core_clock', _('Core Clock (MHz)')),
        ('boost_clock', _('Boost Clock (MHz)')),
        ('tdp', _('TDP (W)')),
        ('socket__name', _('Socket')),
    )


class ProcessorCoolerListView(BaseComponentListView):
    model = ProcessorCooler
    columns = (
        *BASE_COLUMNS,
        ('rpm', _('RPM')),
        ('noise_level', _('Noise Level (db)')),
        ('size', _('Size (cm)')),
        ('socket__name', _('Socket')),
    )


class StorageListView(BaseComponentListView):
    model = Storage
    columns = (
        *BASE_COLUMNS,
        ('capacity', _('Capacity (GB)')),
        ('cache', _('Cache (MB)')),
        ('form_factor__name', _('Form Factor')),
        ('interface__name', _('Interface')),
    )
