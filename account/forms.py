from django import forms
from account.models import *
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = UserAccount
        fields = ['name', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': True}),
            'phone_number': forms.NumberInput(attrs={'required': True}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserAccount.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'required': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'required': True})
    )