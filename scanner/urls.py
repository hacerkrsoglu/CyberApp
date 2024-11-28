from django.urls import path
from . import views

app_name = 'scanner'
urlpatterns = [
    path('', views.scanner, name='scanner'),
    path('approve-url/<int:site_id>/', views.approve_url, name='approve_url'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
