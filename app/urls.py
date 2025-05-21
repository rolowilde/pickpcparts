from django.urls import path, include

import project.settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

if project.settings.DEBUG:  # noinspection PyTypeChecker
    urlpatterns.extend([
        path("__reload__/", include("django_browser_reload.urls")),
    ])
