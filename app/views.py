from django.shortcuts import render

from .models import COMPONENTS, Component


def get_components_total():
    total_components = 0
    for component in COMPONENTS:  # type: Component
        total_components += component.objects.count()
    # naive int flooring
    return int(total_components / 10) * 10


def index(request):
    components_total = get_components_total()
    context = {"components_total": components_total}
    return render(request, 'pickpcparts/index.html', context)
