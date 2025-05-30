from django.urls import path, include

import project.settings
from . import component
from .. import views

urlpatterns = [
    path('', views.home, name='home'),
    path('builder', views.builder, name='builder'),
    path('builds', views.builds, name='builds'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    *component.urlpatterns
]

if project.settings.DEBUG:  # noinspection PyTypeChecker
    urlpatterns.extend([
        path('__reload__/', include("django_browser_reload.urls")),
    ])
