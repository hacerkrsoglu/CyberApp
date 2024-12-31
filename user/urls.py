from django.contrib import admin
from django.urls import path,include
from . import views


app_name = "user"

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('scanner/', include('scanner.urls')),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('profile/', views.profile_view, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
]



    


