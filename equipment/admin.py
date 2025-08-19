from django.contrib import admin
from .models import Brand, ModelEquipment, Equipment, Category, StatusEquipment
from controllers.admin import UserTrackingAdmin


class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand', 'updated_at', 'created_at']
    search_fields = ['brand']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'updated_at', 'created_at']
    search_fields = ['category']


class ModelEquipmentAdmin(UserTrackingAdmin):
    list_display = ['model', 'brand', 'updated_at', 'created_at']
    search_fields = ['model', 'brand']


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'category', 'mac_address',
                    'serial_number', 'status', 'updated_at', 'created_at']
    search_fields = ['brand', 'model', 'category', 'mac_address',
                     'serial_number', 'status']


class StatusEquipmentAdmin(admin.ModelAdmin):
    list_display = ['status', 'updated_at', 'created_at']
    search_fields = ['status', 'updated_at', 'created_at']


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ModelEquipment, ModelEquipmentAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(StatusEquipment, StatusEquipmentAdmin)
