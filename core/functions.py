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
        create_to_controller = [
            ControllerStock(
                equipment=obj,
                location=location,
                reason=reason,
                observation='Equipamento adicionado ao estoque',
                responsible=obj.responsible,
            ) for obj in instance
        ]
        ControllerStock.objects.bulk_create(create_to_controller, update_conflicts=True, update_fields=[
                                            'location', 'reason', 'observation', 'responsible'], unique_fields=['equipment'])

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
    df.columns = df.columns.str.strip().str.lower()
    columns_required = {'brand', 'model', 'category',
                        'mac_address', 'serial_number'}
    if not columns_required.issubset(df.columns):
        missing = columns_required.difference(df.columns)
        return ('erro', f'Colunas obrigatórias faltantes: {', '.join(missing)}')

    # Caches
    brands_models_category = {(normalize(row.brand), normalize(row.model), normalize(row.category)) for row in df[['brand', 'model', 'category']].dropna(
    ).drop_duplicates().itertuples(index=False)}

    # Tratando brands existentes e faltantes
    brands_existing = {obj.brand: obj for obj in Brand.objects.filter(
        brand__in=[normalize(b) for b, _, _ in brands_models_category]
    )}
    missing_brands = {brand for brand, _, _,
                      in brands_models_category if brand not in brands_existing}
    if missing_brands:
        create_brand = [Brand(brand=brand) for brand in missing_brands]
        Brand.objects.bulk_create(create_brand)
        brands_existing.update({obj.brand: obj for obj in create_brand})

    # Tratando categories existentes e faltantes
    category_existing = {obj.category: obj for obj in Category.objects.filter(
        category__in=[normalize(c) for _, _, c in brands_models_category]
    )}
    category_missing = {category for _, _, category,
                        in brands_models_category if category not in category_existing}
    if category_missing:
        create_category = [Category(category=category)
                           for category in category_missing]
        Category.objects.bulk_create(create_category)
        category_existing.update(
            {obj.category: obj for obj in create_category})

    #   Tratando models existentes e faltantes
    models_existing = {obj.model: obj for obj in ModelEquipment.objects.filter(
        model__in=[normalize(m) for _, m, _ in brands_models_category],
        brand__brand__in=[normalize(b) for b, _, _, in brands_models_category],
    )}
    print(models_existing)
    models_missing = {(brand, model) for brand, model,
                      _ in brands_models_category if model and brand not in models_existing}
    print(f'faltantes {models_missing}')
    if models_missing:
        create_model = [ModelEquipment(
            model=model,
            brand=brands_existing.get(brand)
        ) for brand, model in models_missing]
        ModelEquipment.objects.bulk_create(
            create_model,
            update_conflicts=True,
            update_fields=['brand'],
            unique_fields=['model', 'brand']
        )
        models_existing.update({obj.model: obj for obj in create_model})
    # recupera status ativo
    status_active = StatusEquipment.objects.filter(
        status__iexact='ativo').first()
    if not status_active:
        status_active = StatusEquipment.objects.create(status='ATIVO')

    equipment_to_create = [
        Equipment(
            brand=brands_existing.get(normalize(row.brand)),
            model=models_existing.get(normalize(row.model)),
            category=category_existing.get(normalize(row.category)),
            mac_address=normalize(row.mac_address),
            serial_number=normalize(row.serial_number),
            status=status_active,
            responsible=responsible,
        ) for row in df.dropna().itertuples(index=False)
    ]
    print(equipment_to_create)
    Equipment.objects.bulk_create(
        equipment_to_create,
        update_conflicts=True,
        update_fields=['brand', 'model', 'category', 'status', 'responsible'],
        unique_fields=['mac_address']
    )
    create_controller_stock(equipment_to_create)
    return ('success', f'{file.name} carregado com sucesso')
