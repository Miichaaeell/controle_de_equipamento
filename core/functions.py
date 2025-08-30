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
        return ('erro', f'Colunas obrigatórias faltantes: {(', '.join(missing))}')
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
        Brand.objects.bulk_create(
            [Brand(brand=brand) for brand in missing_brands]
        )
        brands_existing.update({obj.brand: obj for obj in Brand.objects.filter(
            brand__in=missing_brands
        )})
    new_brands = len(missing_brands) if missing_brands else 0
    existi_brands = len(brands_existing) - new_brands

    # Tratando categories existentes e faltantes
    category_existing = {obj.category: obj for obj in Category.objects.filter(
        category__in=[normalize(c) for _, _, c in brands_models_category]
    )}
    category_missing = {category for _, _, category,
                        in brands_models_category if category not in category_existing}
    if category_missing:
        Category.objects.bulk_create(
            [Category(category=category) for category in category_missing]
        )
        category_existing.update({obj.category: obj for obj in Category.objects.filter(
            category__in=category_missing
        )})
    new_category = len(category_missing) if category_missing else 0
    existi_category = len(category_existing) - new_category

    #   Tratando models existentes e faltantes
    models_existing = {obj.model: obj for obj in ModelEquipment.objects.filter(
        model__in=[normalize(m) for _, m, _ in brands_models_category])}
    models_missing = {(brand, model) for brand, model,
                      _ in brands_models_category if model not in models_existing}
    if models_missing:
        ModelEquipment.objects.bulk_create(
            [ModelEquipment(
                model=model,
                brand=brands_existing.get(brand)
            ) for brand, model in models_missing]
        )
        models_existing.update({obj.model: obj for obj in ModelEquipment.objects.filter(
            model__in=[model for _, model in models_missing]
        )})
    new_models = len(models_missing) if models_missing else 0
    existi_models = len(models_existing) - new_models

    print(f'Brands: {existi_brands} existentes, {new_brands} novos')
    print(f'Category: {existi_category} existentes, {new_category} novos')
    print(f'Models: {existi_models} existentes, {new_models} novos')

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
    return ('success', f'Realizado {len(equipment_to_create)} novos cadastros')

    # for col_name, cache in [('brand', brands_cache),
    #                         ('category', category_cache),
    #                         ]:
    #     for value in df[col_name].dropna().unique():
    #         key = normalize(value)
    #         if key not in cache:
    #             match col_name:
    #                 case 'brand':
    #                     obj, _ = Brand.objects.get_or_create(brand=key)
    #                 case 'category':
    #                     obj, _ = Category.objects.get_or_create(category=key)
    #             cache[key] = obj
    # # Cria models
    # for row in df[['brand', 'model']].dropna().drop_duplicates().itertuples(index=False):
    #     model = normalize(row.model)
    #     brand = normalize(row.brand)
    #     if model not in models_cache:
    #         obj, _ = ModelEquipment.objects.get_or_create(
    #             model=model,
    #             brand=brands_cache.get(brand)
    #         )
    #         models_cache[model] = obj

    # # Cria lista a ser criada com bulk
    # create_to_equipment = [
    #     Equipment(
    #         brand=brands_cache[normalize(row.brand)],
    #         model=models_cache[normalize(row.model)],
    #         category=category_cache[normalize(row.category)],
    #         mac_address=normalize(row.mac_address),
    #         serial_number=normalize(row.serial_number),
    #         status=status_active,
    #         responsible=responsible,
    #     )for row in df.itertuples(index=False)
    # ]
    # Equipment.objects.bulk_create(create_to_equipment)
    # print(
    #     f'Realizado {len(create_to_equipment)} novos cadastros iniciando registro em controle...')
    # Thread(target=create_controller_stock, args=(create_to_equipment,),
    #        name='ControllerStockImportThread').start()
    # print('Registro em controle sendo processado em segundo plano')
    # return ('success', f'Realizado ')
