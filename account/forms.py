from django import forms
from account.models import *
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = UserAccount
        fields = ['firstname', 'lastname', 'email', 'phonenumber', 'password1', 'password2']
        widgets = {
            'firstname': forms.TextInput(attrs={'required': True, 'placeholder': 'Firstname'}),
            'lastname': forms.TextInput(attrs={'required': True, 'placeholder': 'Lastname'}),
            'email': forms.EmailInput(attrs={'required': True, 'placeholder': 'Email'}),
            'phonenumber': forms.NumberInput(attrs={'required': True, 'placeholder': 'Phone Number'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserAccount.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'required': True, 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'required': True, 'placeholder': 'Enter your password'})
    )