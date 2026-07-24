from django.contrib import admin
from .models import PassportApplication, Payment, Appointment, Document, Notification


@admin.register(PassportApplication)
class PassportApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'application_type', 'status', 'passport_number', 'submitted_at', 'reviewed_by')
    list_filter = ('status', 'application_type')
    search_fields = ('applicant__full_name', 'passport_number')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'amount', 'status', 'receipt_number', 'payment_date')
    list_filter = ('status',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'purpose', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('purpose', 'status')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'document_type', 'is_verified', 'verified_by', 'uploaded_at')
    list_filter = ('document_type', 'is_verified')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'message', 'created_at', 'is_read')
    list_filter = ('is_read',)