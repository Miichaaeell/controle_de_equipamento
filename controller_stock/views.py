from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, UpdateView, CreateView
from core.mixins import FormValidMixin, CreateContextMixin
from .models import ControllerStock, Location, Tracking, Reason
from equipment.models import StatusEquipment, Category
from .forms import ControllerStockForm, ReasonForm


# View Dashboard
class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = ControllerStock.objects.all()
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
                'inactives': inactives,
                'actives': actives,
                'stock': stock.count(),
                'clients': clients.count(),
                'technical': technical.count(),
                'onu_integration': onu_integration.count(),
                'onu': onu.count(),
                'routers': routers.count(),
                'casa_on': casa_on.count()
            }
        }
        return render(request, 'dashboard.html', context)


# Views Controller
class ControllerStockView(LoginRequiredMixin, ListView):
    model = ControllerStock
    template_name = 'controller_stock.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        locations = Location.objects.all()
        context = super().get_context_data(**kwargs)
        context['locations'] = locations
        return context

    def get_queryset(self):
        query_set = super().get_queryset()
        search = self.request.GET.get('search')
        location = self.request.GET.get('location')
        if search:
            query_set = query_set.filter(
                Q(equipment__mac_address__icontains=search) |
                Q(equipment__serial_number__icontains=search)
            )
        if location:
            filter = Location.objects.get(location=location)
            query_set = query_set.filter(
                location=filter
            )

        return query_set


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
class TrackingView(LoginRequiredMixin, ListView):
    model = Tracking
    template_name = 'tracking.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        locations = Location.objects.all()
        context['locations'] = locations
        return context

    def get_queryset(self):
        query_set = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            query_set = query_set.filter(
                Q(equipment__mac_address__icontains=search) |
                Q(equipment__serial_number__icontains=search)
            )
        return query_set


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
