from django.core.management.base import BaseCommand
from equipment.models import Brand, Category, StatusEquipment, ModelEquipment, Equipment
from controller_stock.models import ControllerStock, Tracking, Reason


class Command(BaseCommand):
    help = 'Cleand data base'

    def handle(self, *args, **options):
        for model in [Tracking, ControllerStock, Equipment, ModelEquipment, Brand, Category, StatusEquipment, Reason]:
            model.objects.all().delete()
        print('Data base cleaned')
