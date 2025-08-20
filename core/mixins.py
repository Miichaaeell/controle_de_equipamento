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
        return context
