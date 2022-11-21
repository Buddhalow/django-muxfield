from .fields import MuxField  # NOQA
from django.apps import AppConfig


class MuxfieldConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'muxfield'
