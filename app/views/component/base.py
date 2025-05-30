from typing import Tuple

from django.views.generic import ListView

Columns = Tuple[Tuple[str, str], ...]
BASE_COLUMNS: Columns = (('id', ''), ('manufacturer__name', 'Manufacturer'), ('model', 'Model'))


class BaseComponentListView(ListView):
    template_name = 'pickpcparts/component/list.html'
    columns = BASE_COLUMNS

    @property
    def raw_columns(self):
        ret = tuple(col[0] for col in self.columns)
        return ret

    @property
    def localized_columns(self):
        ret = tuple(col[1] for col in self.columns)
        return ret

    def get_queryset(self):
        return self.model.objects.order_by('manufacturer').values(*self.raw_columns)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = {item.pop('id'): item for item in context['object_list']}
        context.update({
            'columns': self.localized_columns[1:],  # remove id column from UI
            'rows': rows,
        })
        return context
