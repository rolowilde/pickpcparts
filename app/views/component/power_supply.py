from django.db.models import Case, When, Value, CharField

from app.models import PowerSupply
from .base import BaseComponentListView, BASE_COLUMNS


class PowerSupplyListView(BaseComponentListView):
    model = PowerSupply
    columns = (
        *BASE_COLUMNS,
        ('formfactor__name', 'Form Factor'),
        ('wattage', 'Wattage'),
        ('efficiency_label', 'Efficiency'),
        ('modularity_label', 'Modularity'),
    )

    def get_queryset(self):
        # noinspection PyTypeChecker
        return self.model.objects.annotate(
            efficiency_label=Case(
                *[When(efficiency=choice.value, then=Value(choice.label))
                  for choice in PowerSupply.Efficiency],
                default=Value('Unknown'),
                output_field=CharField()
            ),
            modularity_label=Case(
                *[When(modularity=choice.value, then=Value(choice.label))
                  for choice in PowerSupply.Modularity],
                default=Value('Unknown'),
                output_field=CharField()
            )
        ).order_by('manufacturer').values(*self.raw_columns)
