from controller_stock.models import ControllerStock, Reason, Location


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
        equipment__status__status__contains='Inativo')
    actives = data.filter(
        equipment__status__status__contains='Ativo')
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
