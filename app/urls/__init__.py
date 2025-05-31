from django.urls import path, include

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
