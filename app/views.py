from django.shortcuts import render

from .models import COMPONENTS, Component


def get_components_total():
    total_components = 0
    for component in COMPONENTS:  # type: Component
        total_components += component.objects.count()
    # naive int flooring
    return int(total_components / 10) * 10


def home(request):
    components_total = get_components_total()
    context = {"components_total": components_total}
    return render(request, 'pickpcparts/home.html', context)


def builder(request):
    return render(request, 'pickpcparts/builder.html')


def components(request):
    return render(request, 'pickpcparts/components.html')


def builds(request):
    return render(request, 'pickpcparts/builds.html')
