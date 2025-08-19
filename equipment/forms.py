from django import forms
from .models import Equipment, Brand, ModelEquipment, StatusEquipment, Category


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ["brand", "model", "category",
                  "mac_address", "serial_number", "status"]
        widgets = {
            "brand": forms.Select(attrs={
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "model": forms.Select(attrs={
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "category": forms.Select(attrs={
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "mac_address": forms.TextInput(attrs={
                "placeholder": "Ex: AA:BB:CC:DD:EE:FF",
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "serial_number": forms.TextInput(attrs={
                "placeholder": "Digite o serial number",
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "status": forms.Select(attrs={
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["brand"]
        widgets = {
            "brand": forms.TextInput(attrs={
                "placeholder": "Marca",
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            }),
        }


class ModelEquipmentForm(forms.ModelForm):
    class Meta:
        model = ModelEquipment
        fields = ["brand", "model"]
        widgets = {
            "model": forms.TextInput(attrs={
                "placeholder": "Nome do modelo",
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            }),
            "brand": forms.Select(attrs={
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            }),
        }


class StatusEquipmentForm(forms.ModelForm):
    class Meta:
        model = StatusEquipment
        fields = ["status"]
        widgets = {
            "status": forms.TextInput(attrs={
                "placeholder": "Ex: Em uso, Em manutenção, Disponível",
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            }),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category"]
        widgets = {
            "category": forms.TextInput(attrs={
                "placeholder": "Ex: Roteador, Onu, Onu integrada...",
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            }),
        }
