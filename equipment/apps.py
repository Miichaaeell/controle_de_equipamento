from django.apps import AppConfig


class EquipmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'equipment'
    verbose_name='Equipamentos'
    
    def ready(self):
        import equipment.signals