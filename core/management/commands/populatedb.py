import uuid
from django.core.management.base import BaseCommand
from equipment.models import Brand, Category, StatusEquipment, ModelEquipment, Equipment
from controller_stock.models import ControllerStock, Tracking
from django.contrib.auth.models import User
from core.functions import create_controller_stock


class Command(BaseCommand):
    help = 'popular database with fictional data'

    def handle(self, *args, **options):

        # limpar banco antes de popular
        for model in [Tracking, ControllerStock, Equipment, ModelEquipment, Brand, Category, StatusEquipment]:
            model.objects.all().delete()

        # Lista base
        base_list = [
            {'model': 'ec-230', 'brand': 'tp-link', 'category': 'roteador'},
            {'model': 'archer-c6', 'brand': 'tp-link', 'category': 'roteador'},
            {'model': 'ex-511', 'brand': 'tp-link', 'category': 'casa on'},
            {'model': 'ax1800', 'brand': 'xiaomi', 'category': 'roteador'},
            {'model': 'dir-615', 'brand': 'd-link', 'category': 'roteador'},

            {'model': 'hg6145f', 'brand': 'fiberhome', 'category': 'integrada'},
            {'model': 'hg8245h', 'brand': 'huawei', 'category': 'integrada'},
            {'model': 'onu-110', 'brand': 'intelbras', 'category': 'integrada'},

            {'model': 'onu-f601', 'brand': 'fiberhome', 'category': 'onu'},
            {'model': 'hg8010h', 'brand': 'huawei', 'category': 'onu'}
        ]

        # 1 - Criar status
        status_active = StatusEquipment.objects.create(
            status='Ativo')

        # 2 - Criar lista de equipamentos a ser criado e cache
        equipments_to_create = []
        brands_cache = {}
        categories_cache = {}
        models_cache = {}

        responsible = User.objects.all().order_by('date_joined').first()

        if responsible:
            # 3 - Criar brand, Category, Modelos e Equipamento
            for _ in range(200):
                for item in base_list:
                    try:
                        brand = brands_cache.get(
                            item['brand'])
                        if not brand:
                            brand = Brand.objects.create(brand=item['brand'])
                            brands_cache[item['brand']] = brand

                        category = categories_cache.get(item['category'])
                        if not category:
                            category = Category.objects.create(
                                category=item['category'])
                            categories_cache[item['category']] = category

                        model_equipment = models_cache.get(item['model'])
                        if not model_equipment:
                            model_equipment = ModelEquipment.objects.create(
                                model=item['model'],
                                brand=brand,
                            )
                            models_cache[item['model']] = model_equipment

                        equipments_to_create.append(Equipment(
                            brand=brand,
                            model=model_equipment,
                            category=category,
                            mac_address=':'.join(
                                uuid.uuid4().hex[:12][i:i+2] for i in range(0, 12, 2)).upper(),
                            serial_number=uuid.uuid4().hex[:12].upper(),
                            status=status_active,
                            responsible=responsible
                        ))

                    except Exception as e:
                        print(e)
            Equipment.objects.bulk_create(equipments_to_create)
            print(
                f'✅ database successfully populated with {len(equipments_to_create)} registers')
            for equipment in equipments_to_create:
                create_controller_stock(instance=equipment)
            print(
                f'✅ controller stock database successfully populated with {len(equipments_to_create)} registers')
        else:
            print(f'Nenhum usuário cadastrado, para prosseguir, cadastre um usuário')
