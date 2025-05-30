from django.shortcuts import render

from ..models import COMPONENTS


def get_components_total():
    total_components = 0
    for component in COMPONENTS:
        total_components += component.objects.count()
    # naive int flooring
    return int(total_components / 10) * 10


def home(request):
    components_total = get_components_total()
    context = {'components_total': components_total}
    return render(request, 'pickpcparts/home.html', context)


def builder(request):
    return render(request, 'pickpcparts/builder.html')


def builds(request):
    return render(request, 'pickpcparts/builds.html')
