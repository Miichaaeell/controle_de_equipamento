from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tracking, ControllerStock, Location
from equipment.models import Equipment, StatusEquipment


@receiver(post_save, sender=ControllerStock)
def create_tranking(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        try:
            origin = Tracking.objects.filter(
                equipment=instance.equipment).order_by('created_at').last()
            if not origin:
                origin = Location.objects.get(location__icontains='estoque')
            else:
                origin = origin.destination
        except Exception as e:
            print(f'Erro ao obter origin: {e}')
            origin = Location.objects.get(location__icontains='estoque')
        try:
            Tracking.objects.create(
                equipment=instance.equipment,
                origin=origin,
                destination=instance.location,
                reason=instance.reason,
                responsible=instance.responsible,
                observation=instance.observation
            )
        except Exception as e:
            print(f'Erro ao criar Rastreio: {e}')
        if str(instance.location) == 'INATIVO':
            try:
                equipment = Equipment.objects.get(id=instance.equipment.id)
                inactive, _ = StatusEquipment.objects.get_or_create(
                    status='INATIVO')
                equipment.status = inactive
                equipment.save()
            except Exception as e:
                print(e)
