from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username")


class LoginForm(forms.Form):
    email = forms.EmailField(label='E_mail',widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

