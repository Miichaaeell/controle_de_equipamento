from controller_stock.models import ControllerStock, Reason, Location
import pandas as pd


def create_controller_stock(instance):
    location, _ = Location.objects.get_or_create(location='ESTOQUE')
    reason, _ = Reason.objects.get_or_create(reason='ENTRADA')
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
        equipment__category__category__contains='roteador')
    casa_on = data.filter(
        equipment__category__category__contains='casa on')
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


def upload_file(file):
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
                        ('model', models_cache)]:
        for value in df[col_name].unique():
            if value not in cache:
            # cria entidade no banco
                cache[value] = value


    print(brands_cache, models_cache, category_cache)
    return ('success', 'form valid')
