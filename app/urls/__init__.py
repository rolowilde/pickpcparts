from django.urls import path, include

import project.settings
from . import component, build
from .. import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('i18n/', include('django.conf.urls.i18n')),
    *component.urlpatterns,
    *build.urlpatterns,
]

if project.settings.DEBUG:  # noinspection PyTypeChecker
    urlpatterns.extend([
        path('__reload__/', include("django_browser_reload.urls")),
    ])
