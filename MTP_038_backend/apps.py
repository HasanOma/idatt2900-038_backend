from django.apps import AppConfig


class Mtp038BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MTP_038_backend'
    # async def ready(self):
    #     from MTP_038_backend import tasks
    #     await api_requests.main()