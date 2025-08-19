from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from core.mixins import FormValidMixin
from .models import Equipment, Brand, ModelEquipment, Category, StatusEquipment
from .forms import EquipmentForm, BrandForm, ModelEquipmentForm, CategoryForm, StatusEquipmentForm


#Views Equipment
class CreateEquipmentView(FormValidMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'create_equipment.html'
    success_url = reverse_lazy('stock')


#Views Brand
class CreateBrandView(FormValidMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'create_brand.html'
    success_url = reverse_lazy('stock')


#Views Model Equipment
class CreateModelEquipmentView(FormValidMixin, CreateView):
    model = ModelEquipment
    form_class = ModelEquipmentForm
    template_name = 'create_model_equipment.html'
    success_url = reverse_lazy('stock')


#Views Category 
class CreateCategoryView(FormValidMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'create_category.html'
    success_url = reverse_lazy('stock')


#Views Status
class CreateStatusView(FormValidMixin, CreateView):
    model = StatusEquipment
    form_class = StatusEquipmentForm
    template_name = 'create_status_equipment.html'
    success_url = reverse_lazy('stock')