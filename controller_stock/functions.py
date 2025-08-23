from equipment.models import StatusEquipment, Category
from controller_stock.models import Location


def get_metrics(data):
    if data:
        inactives = data.filter(
            equipment__status=StatusEquipment.objects.get(status__icontains='inativo')).count()
        actives = data.count() - inactives
        stock = data.filter(location=Location.objects.get(
            location__icontains='estoque'))
        clients = data.filter(location=Location.objects.get(
            location__icontains='cliente'))
        technical = data.filter(location=Location.objects.get(
            type__icontains='tecnico'))
        onu_integration = data.filter(equipment__category=Category.objects.get(
            category__icontains='ONU Integrada'))
        onu = data.filter(equipment__category=Category.objects.get(
            category='ONU'))
        routers = data.filter(equipment__category=Category.objects.get(
            category__icontains='roteador'))
        casa_on = data.filter(equipment__category=Category.objects.get(
            category__icontains='casa on'))
        context = {
            'metrics': {
                'inactives': inactives if inactives else 0,
                'actives': actives if actives else 0,
                'stock': stock.count() if stock else 0,
                'clients': clients.count() if clients else 0,
                'technical': technical.count() if technical else 0,
                'onu_integration': onu_integration.count() if onu_integration else 0,
                'onu': onu.count() if onu else 0,
                'routers': routers.count() if routers else 0,
                'casa_on': casa_on.count() if casa_on else 0,
            }
        }
    else:
        context = {
            'metrics': {
                'inactives': 0,
                'actives': 0,
                'stock': 0,
                'clients': 0,
                'technical': 0,
                'onu_integration': 0,
                'onu': 0,
                'routers': 0,
                'casa_on': 0,
            }}

    return context
