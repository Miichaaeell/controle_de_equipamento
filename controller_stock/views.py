from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, View, UpdateView, CreateView
from core.mixins import FormValidMixin, CreateContextMixin
from .models import ControllerStock, Location, Tracking, Reason
from .forms import ControllerStockForm, ReasonForm

# View Dashboard


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html')


# Views Controller
class ControllerStockView(ListView):
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


class UpdateControllerStockView(FormValidMixin, CreateContextMixin, UpdateView):
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
class TrackingView(ListView):
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
class CreateReasonView(CreateContextMixin, CreateView):
    model = Reason
    form_class = ReasonForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_reason')


class ListReasonView(CreateContextMixin, ListView):
    model = Reason
    context_object_name = 'object_list'
    template_name = 'components/list.html'


class UpdateReasonView(CreateContextMixin, UpdateView):
    model = Reason
    form_class = ReasonForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_reason')
