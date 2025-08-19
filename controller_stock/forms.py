from django import forms
from .models import ControllerStock


class ControllerStockForm(forms.ModelForm):
    class Meta:
        model = ControllerStock
        fields = ["location", "reason", "observation",
                  "responsible"]  # restrição de fields
        widgets = {
            "location": forms.Select(attrs={
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
                "required": True,
            }),
            "reason": forms.Select(attrs={
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
                "required": True,
            }),
            "observation": forms.Textarea(attrs={
                "class": "mt-1 block w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
                "rows": 3,
                "required": True,
            }),
            "responsible": forms.HiddenInput(),
        }
