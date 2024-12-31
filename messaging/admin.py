# messaging/admin.py
from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'receiver', 'created_at', 'is_read')
    search_fields = ('subject', 'sender__username', 'receiver__username')

admin.site.register(Message, MessageAdmin)
