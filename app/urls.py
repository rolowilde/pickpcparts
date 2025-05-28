from django.urls import path, include

import project.settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('builder', views.builder, name='builder'),
    path('components/processors', views.processors, name='processors'),
    path('components/coolers', views.coolers, name='coolers'),
    path('components/motherboards', views.motherboards, name='motherboards'),
    path('components/memory', views.memory, name='memory'),
    path('components/storage', views.storage, name='storage'),
    path('components/graphics', views.graphics, name='graphics'),
    path('components/power', views.power, name='power'),
    path('components/cases', views.cases, name='cases'),
    path('components/fans', views.fans, name='fans'),
    path('builds', views.builds, name='builds'),
]

if project.settings.DEBUG:  # noinspection PyTypeChecker
    urlpatterns.extend([
        path('__reload__/', include("django_browser_reload.urls")),
    ])
