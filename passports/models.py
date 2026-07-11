from django.db import models
from django.conf import settings
from applicants.models import Applicant
import uuid


class PassportApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,
        related_name='applications'
    )
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