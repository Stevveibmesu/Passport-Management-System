from django import forms
from applicants.models import Applicant
from .models import PassportApplication, Appointment, Document


class PassportApplicationForm(forms.ModelForm):
    class Meta:
        model = PassportApplication
        fields = ['applicant', 'application_type', 'applicant_photo', 'id_document']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        busy_applicant_ids = PassportApplication.objects.exclude(
            status='rejected'
        ).values_list('applicant_id', flat=True)
        self.fields['applicant'].queryset = Applicant.objects.exclude(id__in=busy_applicant_ids)
        self.fields['applicant'].empty_label = "Select an applicant"

    def clean_applicant(self):
        applicant = self.cleaned_data['applicant']
        if PassportApplication.objects.filter(applicant=applicant).exclude(status='rejected').exists():
            raise forms.ValidationError(
                "This applicant already has an active application. "
                "They can only reapply if their previous application was rejected."
            )
        return applicant


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['purpose', 'appointment_date', 'appointment_time', 'location']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file']