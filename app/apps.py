from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
