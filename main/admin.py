from django.contrib import admin
from .models import information
# Register your models here.

class InfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(information, InfoAdmin)
