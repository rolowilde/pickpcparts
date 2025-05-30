from app.models import GraphicsCard
from .base import BaseComponentListView, BASE_COLUMNS


class GraphicsCardListView(BaseComponentListView):
    model = GraphicsCard
    columns = (
        *BASE_COLUMNS,
        ('memory', 'Memory (GB)'),
        ('core_clock', 'Core Clock (MHz)'),
        ('boost_clock', 'Boost Clock (MHz)'),
        ('length', 'Length (cm)'),
    )
