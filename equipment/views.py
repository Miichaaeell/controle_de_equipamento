from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from core.mixins import FormValidMixin, CreateContextMixin
from .models import Equipment, Brand, ModelEquipment, Category, StatusEquipment
from .forms import EquipmentForm, BrandForm, ModelEquipmentForm, CategoryForm, StatusEquipmentForm


# Views Equipment
class CreateEquipmentView(FormValidMixin, CreateContextMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('stock')


class ListEquipmentView(CreateContextMixin, ListView):
    model = Equipment
    template_name = 'components/list.html'
    context_object_name = "object_list"


class UpdateEquipmentView(FormValidMixin, CreateContextMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_equipment')

# Views Brand


class CreateBrandView(FormValidMixin, CreateContextMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('stock')


class ListBrandView(CreateContextMixin, ListView):
    model = Brand
    template_name = 'components/list.html'
    context_object_name = 'object_list'


class UpdateBrandView(FormValidMixin, CreateContextMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_brand')


# Views Model Equipment
class CreateModelEquipmentView(FormValidMixin, CreateContextMixin, CreateView):
    model = ModelEquipment
    form_class = ModelEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_modelequipment')


class ListModelEquipmentView(CreateContextMixin, ListView):
    model = ModelEquipment
    template_name = 'components/list.html'
    context_object_name = 'object_list'


class UpdateModelEquipmentView(FormValidMixin, CreateContextMixin, UpdateView):
    model = ModelEquipment
    form_class = ModelEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_modelequipment')

# Views Category


class CreateCategoryView(FormValidMixin, CreateContextMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_category')


class ListCategoryView(CreateContextMixin, ListView):
    model = Category
    template_name = 'components/list.html'
    context_object_name = 'object_list'


class UpdateCategoryView(FormValidMixin, CreateContextMixin, UpdateView):
    model = Category
    form_class = BrandForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_category')


# Views Status
class CreateStatusEquipmentView(FormValidMixin, CreateContextMixin, CreateView):
    model = StatusEquipment
    form_class = StatusEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_statusequipment')


class ListStatusEquipmentView(CreateContextMixin, ListView):
    model = StatusEquipment
    template_name = 'components/list.html'
    context_object_name = 'object_list'


class UpdateStatusEquipmentView(FormValidMixin, CreateContextMixin, UpdateView):
    model = StatusEquipment
    form_class = StatusEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_statusequipment')
