from app.models import Processor
from .base import BaseComponentListView, BASE_COLUMNS


class ProcessorListView(BaseComponentListView):
    model = Processor
    columns = (
        *BASE_COLUMNS,
        ('core_count', 'Core Count'),
        ('core_clock', 'Core Clock (MHz)'),
        ('boost_clock', 'Boost Clock (MHz)'),
        ('tdp', 'TDP (W)'),
        ('socket__name', 'Socket'),
    )
