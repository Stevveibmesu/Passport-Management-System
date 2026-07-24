from django.db import models
from django.conf import settings
from django.utils import timezone
from applicants.models import Applicant
import uuid


class PassportApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    TYPE_CHOICES = (
        ('new', 'New'),
        ('renewal', 'Renewal'),
        ('correction', 'Correction'),
        ('reissue', 'Reissue (Lost/Damaged)'),
    )

    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    application_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='new')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    passport_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    applicant_photo = models.ImageField(upload_to='applicant_photos/', blank=True, null=True)
    id_document = models.FileField(upload_to='id_documents/', blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )

    def save(self, *args, **kwargs):
        if self.status == 'approved' and not self.passport_number:
            self.passport_number = f"PMS-{uuid.uuid4().hex[:8].upper()}"
        elif self.status != 'approved':
            self.passport_number = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Application #{self.id} - {self.applicant.full_name} ({self.status})"


class Payment(models.Model):
    STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    )

    application = models.OneToOneField(
        PassportApplication,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=3000.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    receipt_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorded_payments'
    )

    def save(self, *args, **kwargs):
        if self.status == 'paid' and not self.receipt_number:
            self.receipt_number = f"RCPT-{uuid.uuid4().hex[:8].upper()}"
            if not self.payment_date:
                self.payment_date = timezone.now()
        elif self.status != 'paid':
            self.receipt_number = None
            self.payment_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.application} - {self.status}"


class Appointment(models.Model):
    PURPOSE_CHOICES = (
        ('biometric', 'Biometric Capture'),
        ('collection', 'Passport Collection'),
    )
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
    )

    application = models.ForeignKey(
        PassportApplication,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='biometric')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    location = models.CharField(max_length=150, default='Main Passport Office')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')

    scheduled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='scheduled_appointments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_purpose_display()} for {self.application.applicant.full_name} on {self.appointment_date}"


class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = (
        ('national_id', 'National ID'),
        ('birth_certificate', 'Birth Certificate'),
        ('photo', 'Passport Photo'),
    )

    application = models.ForeignKey(
        PassportApplication,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='application_documents/')
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_documents'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.application.applicant.full_name}"


class Notification(models.Model):
    application = models.ForeignKey(
        PassportApplication,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.message} ({self.application.applicant.full_name})"