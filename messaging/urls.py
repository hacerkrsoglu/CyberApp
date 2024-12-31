from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('messages/', views.messages_view, name='messages'),
    path('send/', views.send_message, name='send_message'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    
]
