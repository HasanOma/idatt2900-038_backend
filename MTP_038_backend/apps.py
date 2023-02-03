from django.apps import AppConfig
from . import api_requests

class Mtp038BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MTP_038_backend'
    # api_requests.run()