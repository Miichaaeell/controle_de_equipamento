from controller_stock.models import Location, Reason
from django.db.models import Q


class FormValidMixin:
    def form_valid(self, form):
        form.instance.responsible = self.request.user
        return super().form_valid(form)

    filter_technical = False

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.filter_technical == True:
            user = self.request.user
            if self.request.user.groups.filter(name='Tecnico').exists():
                form.fields['location'].queryset = Location.objects.filter(
                    Q(type__icontains='cliente') |
                    Q(type__icontains='estoque') |
                    Q(user=self.request.user))
                form.fields['reason'].queryset = Reason.objects.filter(
                    Q(reason__icontains='troca') |
                    Q(reason__icontains='implanta') |
                    Q(reason__icontains='desativa')
                )
            else:
                form.fields["location"].queryset = Location.objects.all()

        return form


class CreateContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.model._meta.verbose_name}'
        sufix_url = self.model.__name__
        context['sufix_url'] = sufix_url.lower()
        locations = Location.objects.all()
        context['locations'] = locations
        if self.request.user.groups.filter(name__icontains='tecnico'):
            context['is_technical'] = True
        return context


class FilterQuerySetMixin:
    def get_queryset(self):
        query_set = super().get_queryset()
        if self.request.user.groups.filter(name='Tecnico').exists():
            thecnical = Location.objects.get(user=self.request.user)
            query_set = query_set.filter(location=thecnical)
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
