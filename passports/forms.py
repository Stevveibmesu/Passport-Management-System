from django import forms
from .models import PassportApplication


class PassportApplicationForm(forms.ModelForm):
    class Meta:
        model = PassportApplication
        fields = ['applicant', 'applicant_photo', 'id_document']