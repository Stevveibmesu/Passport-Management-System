from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_applicant, name='register_applicant'),
    path('list/', views.applicant_list, name='applicant_list'),
]