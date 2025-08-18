from django.apps import AppConfig


class ControllerStockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'controller_stock'
    verbose_name = 'Controle Estoque'

    def ready(self):
        import controller_stock.signals
