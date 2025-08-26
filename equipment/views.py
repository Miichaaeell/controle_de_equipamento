from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from core.mixins import FormValidMixin, CreateContextMixin, FilterQuerySetMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Equipment, Brand, ModelEquipment, Category, StatusEquipment
from .forms import EquipmentForm, BrandForm, ModelEquipmentForm, CategoryForm, StatusEquipmentForm


# Views Equipment
class CreateEquipmentView(LoginRequiredMixin, PermissionRequiredMixin,  FormValidMixin, CreateContextMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_equipment')
    permission_required = 'equipment.add_equipment'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class ListEquipmentView(LoginRequiredMixin, PermissionRequiredMixin, CreateContextMixin, FilterQuerySetMixin, ListView):
    model = Equipment
    template_name = 'components/list.html'
    context_object_name = "object_list"
    permission_required = 'equipment.view_equipment'
    permission_denied_message = 'Você não tem autorização para acessar está página'
    add_filter = True
    paginate_by = 15


class UpdateEquipmentView(LoginRequiredMixin, PermissionRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_equipment')
    permission_required = 'equipment.change_equipment'
    permission_denied_message = 'Você não tem autorização para acessar está página'


# Views Brand
class CreateBrandView(LoginRequiredMixin, PermissionRequiredMixin, FormValidMixin, CreateContextMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_brand')
    permission_required = 'equipment.add_brand'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class ListBrandView(LoginRequiredMixin, PermissionRequiredMixin, CreateContextMixin, ListView):
    model = Brand
    template_name = 'components/list.html'
    context_object_name = 'object_list'
    permission_required = 'equipment.view_brand'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class UpdateBrandView(LoginRequiredMixin, PermissionRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_brand')
    permission_required = 'equipment.change_brand'
    permission_denied_message = 'Você não tem autorização para acessar está página'


# Views Model Equipment
class CreateModelEquipmentView(LoginRequiredMixin, PermissionRequiredMixin, FormValidMixin, CreateContextMixin, CreateView):
    model = ModelEquipment
    form_class = ModelEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_modelequipment')
    permission_required = 'equipment.add_modelequipment'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class ListModelEquipmentView(LoginRequiredMixin, PermissionRequiredMixin, CreateContextMixin, ListView):
    model = ModelEquipment
    template_name = 'components/list.html'
    context_object_name = 'object_list'
    permission_required = 'equipment.view_modelequipment'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class UpdateModelEquipmentView(LoginRequiredMixin, PermissionRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = ModelEquipment
    form_class = ModelEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_modelequipment')
    permission_required = 'equipment.change_modelequipment'
    permission_denied_message = 'Você não tem autorização para acessar está página'


# Views Category
class CreateCategoryView(LoginRequiredMixin, PermissionRequiredMixin, FormValidMixin, CreateContextMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_category')
    permission_required = 'equipment.add_category'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class ListCategoryView(LoginRequiredMixin, PermissionRequiredMixin, CreateContextMixin, ListView):
    model = Category
    template_name = 'components/list.html'
    context_object_name = 'object_list'
    permission_required = 'equipment.view_category'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class UpdateCategoryView(LoginRequiredMixin, PermissionRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = Category
    form_class = BrandForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_category')
    permission_required = 'equipment.change_category'
    permission_denied_message = 'Você não tem autorização para acessar está página'


# Views Status
class CreateStatusEquipmentView(LoginRequiredMixin, PermissionRequiredMixin, FormValidMixin, CreateContextMixin, CreateView):
    model = StatusEquipment
    form_class = StatusEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_statusequipment')
    permission_required = 'equipment.add_statusequipment'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class ListStatusEquipmentView(LoginRequiredMixin, PermissionRequiredMixin, CreateContextMixin, ListView):
    model = StatusEquipment
    template_name = 'components/list.html'
    context_object_name = 'object_list'
    permission_required = 'equipment.view_statusequipment'
    permission_denied_message = 'Você não tem autorização para acessar está página'


class UpdateStatusEquipmentView(LoginRequiredMixin, PermissionRequiredMixin, FormValidMixin, CreateContextMixin, UpdateView):
    model = StatusEquipment
    form_class = StatusEquipmentForm
    template_name = 'components/create_update_model.html'
    success_url = reverse_lazy('list_statusequipment')
    permission_required = 'equipment.change_statusequipment'
    permission_denied_message = 'Você não tem autorização para acessar está página'
