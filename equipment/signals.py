from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Equipment
from core.functions import create_controller_stock
from controller_stock.models import ControllerStock, Location


@receiver(post_save, sender=Equipment)
def create_equipment_in_stock(sender, instance, created, **kwargs):
    if created:
        try:
            create_controller_stock(instance=instance)
        except Exception as e:
            print(e)
