from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('officers/', views.officer_list, name='officer_list'),
    path('officers/add/', views.add_officer, name='add_officer'),
    path('officers/<int:pk>/toggle/', views.toggle_officer_status, name='toggle_officer_status'),
]