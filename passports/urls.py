from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_application, name='submit_application'),
    path('list/', views.application_list, name='application_list'),
    path('<int:pk>/update/', views.update_status, name='update_status'),
    path('<int:pk>/payment/', views.record_payment, name='record_payment'),
    path('<int:pk>/appointments/schedule/', views.schedule_appointment, name='schedule_appointment'),
    path('<int:pk>/appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:appointment_pk>/status/', views.update_appointment_status, name='update_appointment_status'),
    path('<int:pk>/documents/', views.document_list, name='document_list'),
    path('documents/<int:document_pk>/verify/', views.verify_document, name='verify_document'),
    path('<int:pk>/notifications/', views.notification_list, name='notification_list'),
    path('<int:pk>/delete/', views.delete_application, name='delete_application'),
]