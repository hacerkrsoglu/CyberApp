from django.urls import path
from . import views

app_name = 'scanner'
urlpatterns = [
    path('', views.scanner, name='scanner'),
    path('start_scan/<int:site_id>/', views.start_scan, name='start_scan'),
    path('scan_results/<int:site_id>/', views.scan_results, name='scan_results'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve_url/<int:site_id>/', views.approve_url, name='approve_url'),
]
