from equipment.models import Brand, Category, ModelEquipment, Equipment, StatusEquipment
from controller_stock.models import ControllerStock, Reason, Location
import pandas as pd
from collections.abc import Iterable
from threading import Thread


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
    try:
        match ext:
            case 'xlsx':
                df = pd.read_excel(file)
            case 'csv':
                df = pd.read_csv(file)
    except Exception as e:
        return ('erro', f'Erro ao ler o arquivo: {str(e)}')

    df.columns = df.columns.str.strip().str.lower()
    columns_required = {'brand', 'model', 'category',
                        'mac_address', 'serial_number'}
    if not columns_required.issubset(df.columns):
        missing = columns_required.difference(df.columns)
        return ('erro', f'Colunas obrigatórias faltantes: {', '.join(missing)}')

    # Padronizando textos para maiusculo
    df = df.apply(lambda x: x.str.upper())

    # Tratando brands existentes e faltantes
    unique_brands = set(df['brand'].dropna().unique())
    brands_existing = {obj.brand: obj for obj in Brand.objects.filter(
        brand__in=[brand for brand in unique_brands]
    )}

    missing_brands = unique_brands.difference(brands_existing.keys())
    if missing_brands:
        create_brand = [Brand(brand=brand) for brand in missing_brands]
        Brand.objects.bulk_create(create_brand)
        brands_existing.update({obj.brand: obj for obj in create_brand})

    # Tratando categories existentes e faltantes
    unique_categorys = set(df['category'].dropna().unique())
    category_existing = {obj.category: obj for obj in Category.objects.filter(
        category__in=[category for category in unique_categorys]
    )}
    category_missing = unique_categorys.difference(category_existing.keys())
    if category_missing:
        create_category = [Category(category=category)
                           for category in category_missing]
        Category.objects.bulk_create(create_category)
        category_existing.update(
            {obj.category: obj for obj in create_category})

    # Tratando models existentes e faltantes
    models_existing = dict()
    models_missing = []
    brands_models = df[['brand', 'model']].dropna().drop_duplicates().itertuples(
        index=False)
    brand_models_in_db = ModelEquipment.objects.all(
    ).select_related('brand')  # QuerySet unica ao banco
    for brand, model in brands_models:
        obj = brand_models_in_db.filter(
            model=model,
            brand__brand=brand
        ).first()
        if obj:
            models_existing[model] = obj
        else:
            models_missing.append((brand, model))

    create_models = [ModelEquipment(
        model=model,
        brand=brands_existing.get(brand),
    ) for brand, model in models_missing]
    ModelEquipment.objects.bulk_create(create_models)
    models_existing.update({obj.model: obj for obj in create_models})

    # recupera status ativo
    status_active = StatusEquipment.objects.filter(
        status__iexact='ativo').first()
    if not status_active:
        status_active = StatusEquipment.objects.create(status='ATIVO')
    equipemnts_existing = list(Equipment.objects.filter(
        mac_address__in=df['mac_address'].dropna().unique()))
    # Criando equipamentos
    equipment_to_create = [
        Equipment(
            brand=brands_existing.get(row.brand),
            model=models_existing.get(row.model),
            category=category_existing.get(row.category),
            mac_address=row.mac_address,
            serial_number=row.serial_number,
            status=status_active,
            responsible=responsible,
        ) for row in df.dropna().itertuples(index=False) if row.mac_address not in {eq.mac_address for eq in equipemnts_existing}
    ]
    print(f'Equipamentos a criar: {len(equipment_to_create)}')
    Equipment.objects.bulk_create(
        equipment_to_create,
        update_conflicts=True,
        update_fields=['brand', 'model', 'category', 'status', 'responsible'],
        unique_fields=['mac_address']
    )
    create_controller_stock(equipment_to_create)
    total_created = len(missing_brands) + \
        len(category_missing) + len(models_missing) + len(equipment_to_create)
    total_existing = len(df) - len(equipment_to_create)
    return ('success', f'''{file.name} carregado com sucesso,\n
            {len(missing_brands)} marcas criadas,\n
            {len(brands_existing) - len(missing_brands)} marcas já existentes no sistema,\n
            {len(category_missing)} categorias criadas,\n
            {len(category_existing) - len(category_missing)} categorias já existentes no sistema,\n
            {len(models_missing)} modelos criados,\n
            {len(models_existing) - len(models_missing)} modelos já existentes no sistema,\n
            {len(equipment_to_create)} equipamentos criados,\n
            {total_existing} equipamentos já existentes no sistema.\n
            {total_created} registros criados no total.
            ''')
