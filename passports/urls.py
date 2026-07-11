from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_application, name='submit_application'),
    path('list/', views.application_list, name='application_list'),
    path('<int:pk>/update/', views.update_status, name='update_status'),
]