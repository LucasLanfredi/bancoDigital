from django.apps import AppConfig

class WalletApiDjango2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallet_api_django2'

    def ready(self):
        import wallet_api_django2.signals