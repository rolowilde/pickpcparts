from app.models import CaseFan
from .base import BaseComponentListView, BASE_COLUMNS


class CaseFanListView(BaseComponentListView):
    model = CaseFan
    columns = (
        *BASE_COLUMNS,
        ('size', 'Size'),
        ('rpm', 'RPM'),
        ('noise_level', 'Noise Level (db)'),
        ('pwm', 'PWM'),
    )
