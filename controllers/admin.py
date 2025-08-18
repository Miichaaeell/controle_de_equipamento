from django.contrib import admin

class UserTrackingAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save(responsible=request.user)

    
