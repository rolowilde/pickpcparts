from app.models import Storage
from .base import BaseComponentListView, BASE_COLUMNS


class StorageListView(BaseComponentListView):
    model = Storage
    columns = (
        *BASE_COLUMNS,
        ('capacity', 'Capacity (GB)'),
        ('cache', 'Cache (MB)'),
        ('form_factor__name', 'Form Factor'),
        ('interface__name', 'Interface'),
    )
