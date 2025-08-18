from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, View
from .models import ControllerStock, Location


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html')


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
