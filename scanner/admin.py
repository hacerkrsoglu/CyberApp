from django.contrib import admin
from .models import Scanner

class ScannerAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'approval_status', 'created_at', 'updated_at')

admin.site.register(Scanner, ScannerAdmin)
