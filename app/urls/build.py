from django.urls import path

from ..views import build

urlpatterns = [
    path('build/', build.BuildListView.as_view(), name='builds'),
    path('build/create/', build.BuildCreateView.as_view(), name='build-create'),
    path('build/<int:pk>/', build.BuildDetailView.as_view(), name='build-detail'),
    path('build/<int:pk>/update/', build.BuildUpdateView.as_view(), name='build-update'),
    path('build/<int:pk>/delete/', build.BuildDeleteView.as_view(), name='build-delete'),
]
