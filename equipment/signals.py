from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Equipment
from controller_stock.models import ControllerStock, Reason, Location


@receiver(post_save, sender=Equipment)
def create_equipment_in_stock(sender, instance, created, **kwargs):
    if created:
        try:
            ControllerStock.objects.create(
                equipment=instance,
                location=Location.objects.get(location__icontains='estoque'),
                reason=Reason.objects.get(reason__icontains='entrada'),
                observation='Equipamento adicionado ao estoque',
                responsible=instance.responsible,
            )
        except Exception as e:
            print(e)
