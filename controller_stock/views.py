from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, UpdateView, CreateView
from core.mixins import FormValidMixin, CreateContextMixin, FilterQuerySetMixin
from .models import ControllerStock, Location, Tracking, Reason
from equipment.models import StatusEquipment, Category
from .forms import ControllerStockForm, ReasonForm


# View Dashboard
class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = ControllerStock.objects.all()
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
        return render(request, 'dashboard.html', context)


# Views Controller
class ControllerStockView(LoginRequiredMixin, FilterQuerySetMixin, CreateContextMixin, ListView):
    model = ControllerStock
    template_name = 'controller_stock.html'
    paginate_by = 10


class UpdateControllerStockView(LoginRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = ControllerStock
    form_class = ControllerStockForm
    template_name = 'update_controller.html'
    success_url = reverse_lazy('stock')

    def get_initial(self):
        initial = super().get_initial()
        # força campos a iniciarem vazios
        initial["location"] = None
        initial["reason"] = ""
        initial["observation"] = ""
        return initial


# View Tracking
class TrackingView(LoginRequiredMixin, FilterQuerySetMixin, ListView):
    model = Tracking
    template_name = 'tracking.html'
    paginate_by = 10


# Views Reason
class CreateReasonView(LoginRequiredMixin, CreateContextMixin, CreateView):
    model = Reason
    form_class = ReasonForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_reason')


class ListReasonView(LoginRequiredMixin, CreateContextMixin, ListView):
    model = Reason
    context_object_name = 'object_list'
    template_name = 'components/list.html'


class UpdateReasonView(LoginRequiredMixin, CreateContextMixin, UpdateView):
    model = Reason
    form_class = ReasonForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_reason')
