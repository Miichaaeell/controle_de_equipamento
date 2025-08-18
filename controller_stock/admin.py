from django.contrib import admin
from .models import Location, ControllerStock, Reason, Tracking


class ControllerStockAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'equipment__mac_address', 'equipment__serial_number', 'location',
                    'reason', 'observation', 'responsible', 'updated_at', 'created_at']
    search_fields = ['equipment__mac_address', 'equipment__serial_number',
                     'location__location', 'reason__reason']
    list_filter = ['equipment__category',
                   'location__location', 'equipment__status']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['location', 'type', 'updated_at', 'created_at']
    search_fields = ['location', 'type']


class ReasonAdmin(admin.ModelAdmin):
    list_display = ['reason', 'updated_at', 'created_at']
    search_fields = ['reason']


class TrackingAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'equipment__mac_address', 'equipment__serial_number', 'origin',
                    'destination', 'reason', 'observation', 'responsible', 'created_at']
    search_fields = ['equipment__mac_address',
                     'equipment__serial_number',]
    list_filter = ['reason', 'equipment__category']


admin.site.register(Location, LocationAdmin)
admin.site.register(ControllerStock, ControllerStockAdmin)
admin.site.register(Reason, ReasonAdmin)
admin.site.register(Tracking, TrackingAdmin)
