from django.contrib import admin
from .models import Branch, ModelEquipment, Equipment, Category, StatusEquipment
from controllers.admin import UserTrackingAdmin


class BranchAdmin(admin.ModelAdmin):
    list_display = ['branch', 'updated_at', 'created_at']
    search_fields = ['branch']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'updated_at', 'created_at']
    search_fields = ['category']


class ModelEquipmentAdmin(UserTrackingAdmin):
    list_display = ['model', 'branch', 'updated_at', 'created_at']
    search_fields = ['model', 'branch']


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['branch', 'model', 'category', 'mac_address',
                    'serial_number', 'status', 'updated_at', 'created_at']
    search_fields = ['branch', 'model', 'category', 'mac_address',
                     'serial_number', 'status']


class StatusEquipmentAdmin(admin.ModelAdmin):
    list_display = ['status', 'updated_at', 'created_at']
    search_fields = ['status', 'updated_at', 'created_at']


admin.site.register(Branch, BranchAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ModelEquipment, ModelEquipmentAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(StatusEquipment, StatusEquipmentAdmin)
