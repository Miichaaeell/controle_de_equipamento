from equipment.models import Brand, Category, ModelEquipment, Equipment, StatusEquipment
from controller_stock.models import ControllerStock, Reason, Location
import pandas as pd
from collections.abc import Iterable
from threading import Thread


def normalize(text: str) -> str:
    return text.strip().upper()


def create_controller_stock(instance):
    location, _ = Location.objects.get_or_create(location='ESTOQUE')
    reason, _ = Reason.objects.get_or_create(reason='ENTRADA')
    if isinstance(instance, Iterable) and not isinstance(instance, (str, bytes)):
        for obj in instance:
            ControllerStock.objects.create(
                equipment=obj,
                location=location,
                reason=reason,
                observation='Equipamento adicionado ao estoque',
                responsible=obj.responsible,
            )
    else:
        ControllerStock.objects.create(
            equipment=instance,
            location=location,
            reason=reason,
            observation='Equipamento adicionado ao estoque',
            responsible=instance.responsible,
        )


def get_metrics(data):
    inactives = data.filter(
        equipment__status__status__iexact='inativo')
    actives = data.filter(
        equipment__status__status__iexact='ativo')
    stock = data.filter(location__location__icontains='estoque')
    clients = data.filter(location__location__icontains='cliente')
    technical = data.filter(location__type__icontains='tecnico')
    integration = data.filter(
        equipment__category__category__icontains='integrada')
    onu = data.filter(equipment__category__category__icontains='onu')
    routers = data.filter(
        equipment__category__category__icontains='roteador')
    casa_on = data.filter(
        equipment__category__category__icontains='casa on')
    context = {
        'metrics': {
            'inactives': inactives.count() if inactives else 0,
            'actives': actives.count() if actives else 0,
            'stock': stock.count() if stock else 0,
            'clients': clients.count() if clients else 0,
            'technical': technical.count() if technical else 0,
            'onu_integration': integration.count() if integration else 0,
            'onu': onu.count() if onu else 0,
            'routers': routers.count() if routers else 0,
            'casa_on': casa_on.count() if casa_on else 0,
        }
    }

    return context


def upload_file(file, responsible):
    # 1. verificar extensão
    ext = file.name.split('.')[-1].lower()
    if ext not in ['xlsx', 'csv']:
        return ('erro', 'Formato de arquivo inválido')
    match ext:
        case 'xlsx':
            df = pd.read_excel(file)
        case 'csv':
            df = pd.read_csv(file)
    columns_required = {'brand', 'model', 'category',
                        'mac_address', 'serial_number'}
    if not columns_required.issubset(df.columns):
        return ('erro', 'Estrutura do arquivo incompátivel')
    brands_cache, category_cache, models_cache = {}, {}, {}

    for col_name, cache in [('brand', brands_cache),
                            ('category', category_cache),
                            ]:
        for value in df[col_name].dropna().unique():
            key = normalize(value)
            if key not in cache:
                match col_name:
                    case 'brand':
                        obj, _ = Brand.objects.get_or_create(brand=key)
                    case 'category':
                        obj, _ = Category.objects.get_or_create(category=key)
            cache[key] = obj
    # Cria models
    for row in df[['brand', 'model']].dropna().drop_duplicates().itertuples(index=False):
        model = normalize(row.model)
        brand = normalize(row.brand)
        if model not in models_cache:
            obj, _ = ModelEquipment.objects.get_or_create(
                model=model,
                brand=brands_cache.get(brand)
            )
            models_cache[model] = obj
    # recupera status ativo
    status_active = StatusEquipment.objects.filter(
        status__iexact='ativo').first()
    if not status_active:
        status_active = StatusEquipment.objects.create(status='ATIVO')
    # Cria lista a ser criada com bulk
    create_to_equipment = [
        Equipment(
            brand=brands_cache[normalize(row.brand)],
            model=models_cache[normalize(row.model)],
            category=category_cache[normalize(row.category)],
            mac_address=normalize(row.mac_address),
            serial_number=normalize(row.serial_number),
            status=status_active,
            responsible=responsible,
        )for row in df.itertuples(index=False)
    ]
    Equipment.objects.bulk_create(create_to_equipment)
    Thread(target=create_controller_stock, args=(create_to_equipment,),
           name='ControllerStockImportThread').start()
    print(f'Realizado {len(create_to_equipment)} novos cadastros')
    return ('success', f'Realizado {len(create_to_equipment)} novos cadastros')
