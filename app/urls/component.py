from django.urls import path

from ..views import component

urlpatterns = [
    path('components/processor', component.ProcessorListView.as_view(), name='component-processor-list'),
    path('components/cooler', component.ProcessorCoolerListView.as_view(), name='component-cooler-list'),
    path('components/motherboard', component.MotherboardListView.as_view(), name='component-motherboard-list'),
    path('components/memory', component.MemoryListView.as_view(), name='component-memory-list'),
    path('components/storage', component.StorageListView.as_view(), name='component-storage-list'),
    path('components/graphics', component.GraphicsCardListView.as_view(), name='component-graphics-list'),
    path('components/power', component.PowerSupplyListView.as_view(), name='component-power-list'),
    path('components/case', component.CaseListView.as_view(), name='component-case-list'),
    path('components/fan', component.CaseFanListView.as_view(), name='component-fan-list'),
]
