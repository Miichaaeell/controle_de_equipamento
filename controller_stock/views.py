from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, View, UpdateView, CreateView
from core.mixins import FormValidMixin, CreateContextMixin, FilterQuerySetMixin
from .models import ControllerStock, Tracking, Reason
from .forms import ControllerStockForm, ReasonForm
from .functions import get_metrics


# View Dashboard
class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = [
        'controller_stock.view_controllerstock',
        'controller_stock.add_controllerstock',
    ]
    permission_denied_message = 'Você não tem autorização para acessar está página'

    def get(self, request, *args, **kwargs):
        data = ControllerStock.objects.all()
        context = get_metrics(data)
        return render(request, 'dashboard.html', context)


# Views Controller
class ControllerStockView(LoginRequiredMixin, PermissionRequiredMixin, FilterQuerySetMixin, CreateContextMixin, ListView):
    model = ControllerStock
    template_name = 'controller_stock.html'
    paginate_by = 10
    permission_required = 'controller_stock.view_controllerstock'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class UpdateControllerStockView(LoginRequiredMixin, PermissionRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = ControllerStock
    form_class = ControllerStockForm
    template_name = 'update_controller.html'
    permission_required = 'controller_stock.change_controllerstock'
    success_url = reverse_lazy('stock')
    permission_denied_message = 'Você não tem autorização para acessar está página'
    filter_technical = True

    def get_initial(self):
        initial = super().get_initial()
        # força campos a iniciarem vazios
        initial["location"] = None
        initial["reason"] = ""
        initial["observation"] = ""
        return initial


# View Tracking
class TrackingView(LoginRequiredMixin, PermissionRequiredMixin, FilterQuerySetMixin, ListView):
    model = Tracking
    template_name = 'tracking.html'
    paginate_by = 10
    permission_required = 'controller_stock.view_tracking'
    permission_denied_message = 'Você não tem autorização para acessar está página'


# Views Reason
class CreateReasonView(LoginRequiredMixin, PermissionRequiredMixin, CreateContextMixin, CreateView):
    model = Reason
    form_class = ReasonForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_reason')
    permission_required = 'controller_stock.add_reason'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class ListReasonView(LoginRequiredMixin, PermissionRequiredMixin, CreateContextMixin, ListView):
    model = Reason
    context_object_name = 'object_list'
    template_name = 'components/list.html'
    permission_required = 'controller_stock.view_reason'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class UpdateReasonView(LoginRequiredMixin, PermissionRequiredMixin, CreateContextMixin, UpdateView):
    model = Reason
    form_class = ReasonForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_reason')
    permission_required = 'controller_stock.change_reason'
    permission_denied_message = 'Você não tem autorização para acessar está página'
