from controller_stock.models import Location
from django.db.models import Q


class FormValidMixin:
    def form_valid(self, form):
        form.instance.responsible = self.request.user
        return super().form_valid(form)


class CreateContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.model._meta.verbose_name}'
        sufix_url = self.model.__name__
        context['sufix_url'] = sufix_url.lower()
        locations = Location.objects.all()
        context['locations'] = locations
        return context


class FilterQuerySetMixin:
    def get_queryset(self):
        query_set = super().get_queryset()
        try:
            search = self.request.GET.get('search')
        except:
            pass
        try:
            location = self.request.GET.get('location')
        except:
            pass
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
