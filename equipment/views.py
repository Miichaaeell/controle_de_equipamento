from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from core.mixins import FormValidMixin, CreateContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Equipment, Brand, ModelEquipment, Category, StatusEquipment
from .forms import EquipmentForm, BrandForm, ModelEquipmentForm, CategoryForm, StatusEquipmentForm


# Views Equipment
class CreateEquipmentView(LoginRequiredMixin, FormValidMixin, CreateContextMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_equipment')


class ListEquipmentView(LoginRequiredMixin, CreateContextMixin, ListView):
    model = Equipment
    template_name = 'components/list.html'
    context_object_name = "object_list"


class UpdateEquipmentView(LoginRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_equipment')

# Views Brand


class CreateBrandView(LoginRequiredMixin, FormValidMixin, CreateContextMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_brand')


class ListBrandView(LoginRequiredMixin, CreateContextMixin, ListView):
    model = Brand
    template_name = 'components/list.html'
    context_object_name = 'object_list'


class UpdateBrandView(LoginRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_brand')


# Views Model Equipment
class CreateModelEquipmentView(LoginRequiredMixin, FormValidMixin, CreateContextMixin, CreateView):
    model = ModelEquipment
    form_class = ModelEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_modelequipment')


class ListModelEquipmentView(LoginRequiredMixin, CreateContextMixin, ListView):
    model = ModelEquipment
    template_name = 'components/list.html'
    context_object_name = 'object_list'


class UpdateModelEquipmentView(LoginRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = ModelEquipment
    form_class = ModelEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_modelequipment')

# Views Category


class CreateCategoryView(LoginRequiredMixin, FormValidMixin, CreateContextMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_category')


class ListCategoryView(LoginRequiredMixin, CreateContextMixin, ListView):
    model = Category
    template_name = 'components/list.html'
    context_object_name = 'object_list'


class UpdateCategoryView(LoginRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = Category
    form_class = BrandForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_category')


# Views Status
class CreateStatusEquipmentView(LoginRequiredMixin, FormValidMixin, CreateContextMixin, CreateView):
    model = StatusEquipment
    form_class = StatusEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_statusequipment')


class ListStatusEquipmentView(LoginRequiredMixin, CreateContextMixin, ListView):
    model = StatusEquipment
    template_name = 'components/list.html'
    context_object_name = 'object_list'


class UpdateStatusEquipmentView(LoginRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = StatusEquipment
    form_class = StatusEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_statusequipment')
