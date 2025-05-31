from django.core.serializers import serialize
from django.http import JsonResponse


class JSONResponseMixin:
    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_json_data(context),
            safe=False,
            **response_kwargs
        )

    def get_json_data(self, context):
        if 'object_list' in context:
            return self.serialize_queryset(context['object_list'])
        elif 'object' in context:
            return self.serialize_instance(context['object'])
        return context

    def serialize_queryset(self, queryset):
        serialized = serialize('python', queryset)
        return [
            self.enrich_object_data(obj_data)
            for obj_data in serialized
        ]

    def serialize_instance(self, instance):
        serialized = serialize('python', [instance])
        return self.enrich_object_data(serialized[0])

    def enrich_object_data(self, obj_data):
        model = obj_data['model']
        pk = obj_data['pk']
        fields = obj_data['fields']

        if hasattr(self, 'get_absolute_url'):
            fields['url'] = self.get_absolute_url()

        fields['_type'] = model.split('.')[-1]
        return fields
