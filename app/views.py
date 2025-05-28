from django.db.models import F, When, Value, Case as _Case, CharField
from django.shortcuts import render

from .models import COMPONENTS, Processor, ProcessorCooler, Motherboard, Memory, Storage, GraphicsCard, PowerSupply, \
    Case, CaseFan

COMPONENT_COLUMNS = ("Manufacturer", "Model")
COMPONENT_ROWS = ("manufacturer__name", "model")


def get_components_total():
    total_components = 0
    for component in COMPONENTS:
        total_components += component.objects.count()
    # naive int flooring
    return int(total_components / 10) * 10


def render_component_list(request, columns, rows):
    context = {"columns": columns, "rows": rows}
    return render(request, 'pickpcparts/_component_list_base.html', context)


def home(request):
    components_total = get_components_total()
    context = {"components_total": components_total}
    return render(request, 'pickpcparts/home.html', context)


def builder(request):
    return render(request, 'pickpcparts/builder.html')


def processors(request):
    columns = (*COMPONENT_COLUMNS, "Core Count", "Core Clock (MHz)", "Boost Clock (MHz)", "TDP (W)", "Socket")
    rows = (Processor.objects.all().order_by('manufacturer').values(
        *COMPONENT_ROWS,
        'core_count',
        'core_clock',
        'boost_clock',
        'tdp',
        'socket__name'))
    return render_component_list(request, columns, rows)


def coolers(request):
    columns = (*COMPONENT_COLUMNS, "RPM", "Noise Level (db)", "Size (cm)", "Socket")
    rows = (ProcessorCooler.objects.all().order_by('manufacturer').values(
        *COMPONENT_ROWS,
        'rpm',
        'noise_level',
        'size',
        'socket__name'
    ))
    return render_component_list(request, columns, rows)


def motherboards(request):
    columns = (*COMPONENT_COLUMNS, "Max Memory (GB)", "Memory Slots", "Supported Memory", "Form Factor", "Socket")
    rows = (Motherboard.objects.all().order_by('manufacturer').values(
        *COMPONENT_ROWS,
        'max_memory',
        'memory_slots',
        'supported_memory__name',
        'formfactor__name',
        'socket__name'
    ))
    return render_component_list(request, columns, rows)


def memory(request):
    columns = (*COMPONENT_COLUMNS, "Total Capacity (GB)", "Modules", "Speed (MT/s)", "First Word Latency (ns)",
               "CAS Latency (ns)",
               "Type")
    rows = (Memory.objects.annotate(capacity=F('capacity_per_module') * F('modules')).all().order_by(
        'manufacturer').values(
        *COMPONENT_ROWS,
        'capacity',
        'modules',
        'speed',
        'first_word_latency',
        'cas_latency',
        'type__name'
    ))
    return render_component_list(request, columns, rows)


def storage(request):
    columns = (*COMPONENT_COLUMNS, "Capacity (GB)", "Cache (MB)", "Form Factor", "Interface")
    rows = (Storage.objects.all().order_by(
        'manufacturer').values(
        *COMPONENT_ROWS,
        'capacity',
        'cache',
        'form_factor__name',
        'interface__name'
    ))
    return render_component_list(request, columns, rows)


def graphics(request):
    columns = (*COMPONENT_COLUMNS, "Memory (GB)", "Core Clock (MHz)", "Boost Clock (MHz)", "Length (cm)")
    rows = (GraphicsCard.objects.all().order_by('manufacturer').values(
        *COMPONENT_ROWS,
        'memory',
        'core_clock',
        'boost_clock',
        'length',
    ))
    return render_component_list(request, columns, rows)


def power(request):
    columns = (*COMPONENT_COLUMNS, "Form Factor", "Wattage", "Efficiency", "Modularity")
    # noinspection PyTypeChecker
    rows = (PowerSupply.objects.annotate(
        efficiency_label=_Case(
            *[
                When(efficiency=choice.value, then=Value(choice.label))
                for choice in PowerSupply.Efficiency
            ],
            default=Value('Unknown'),
            output_field=CharField()
        ),
        modularity_label=_Case(
            *[
                When(modularity=choice.value, then=Value(choice.label))
                for choice in PowerSupply.Modularity
            ],
            default=Value('Unknown'),
            output_field=CharField()
        )
    ).all().order_by('manufacturer').values(
        *COMPONENT_ROWS,
        'formfactor__name',
        'wattage',
        'efficiency_label',
        'modularity_label',
    ))
    return render_component_list(request, columns, rows)


def cases(request):
    columns = [*COMPONENT_COLUMNS, 'Form Factor', 'External Volume']
    rows = (Case.objects.all().order_by('manufacturer').values(
        *COMPONENT_ROWS,
        'formfactor__name',
        'external_volume'))
    return render_component_list(request, columns, rows)


def fans(request):
    columns = [*COMPONENT_COLUMNS, 'Size', 'RPM', 'Noise Level (db)', 'PWM']
    rows = (CaseFan.objects.all().order_by('manufacturer').values(
        *COMPONENT_ROWS,
        'size',
        'rpm',
        'noise_level',
        'pwm'))
    return render_component_list(request, columns, rows)


def builds(request):
    return render(request, 'pickpcparts/builds.html')
