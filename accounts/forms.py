from django.contrib.auth.forms import UserCreationForm
from .models import User


class OfficerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number', 'role')