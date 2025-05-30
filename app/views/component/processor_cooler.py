from app.models import ProcessorCooler
from .base import BaseComponentListView, BASE_COLUMNS


class ProcessorCoolerListView(BaseComponentListView):
    model = ProcessorCooler
    columns = (
        *BASE_COLUMNS,
        ('rpm', 'RPM'),
        ('noise_level', 'Noise Level (db)'),
        ('size', 'Size (cm)'),
        ('socket__name', 'Socket'),
    )
