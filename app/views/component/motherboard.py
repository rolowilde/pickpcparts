from app.models import Motherboard
from .base import BaseComponentListView, BASE_COLUMNS


class MotherboardListView(BaseComponentListView):
    model = Motherboard
    columns = (
        *BASE_COLUMNS,
        ('max_memory', 'Max Memory (GB)'),
        ('memory_slots', 'Memory Slots'),
        ('supported_memory__name', 'Supported Memory'),
        ('formfactor__name', 'Form Factor'),
        ('socket__name', 'Socket'),
    )
