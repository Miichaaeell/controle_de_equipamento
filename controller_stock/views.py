from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, UpdateView, CreateView
from core.mixins import FormValidMixin, CreateContextMixin, FilterQuerySetMixin
from .models import ControllerStock, Tracking, Reason
from .forms import ControllerStockForm, ReasonForm
from .functions import get_metrics


# View Dashboard
class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = ControllerStock.objects.all()
        context = get_metrics(data)
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
