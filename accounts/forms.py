from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class OfficerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number', 'role')


class OfficerEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'role')