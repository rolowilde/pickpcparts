from app.models import Case
from .base import BaseComponentListView, BASE_COLUMNS


class CaseListView(BaseComponentListView):
    model = Case
    columns = (
        *BASE_COLUMNS,
        ('formfactor__name', 'Form Factor'),
        ('external_volume', 'External Volume'),
    )
