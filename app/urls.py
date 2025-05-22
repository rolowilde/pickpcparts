from django.urls import path, include

import project.settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('builder', views.builder, name='builder'),
    path('components', views.components, name='components'),
    path('builds', views.builds, name='builds'),
]

if project.settings.DEBUG:  # noinspection PyTypeChecker
    urlpatterns.extend([
        path('__reload__/', include("django_browser_reload.urls")),
    ])
