from django import forms
from home.models import *

STAR_CHOICES = [
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
]

class RoomReviewForm(forms.ModelForm):
    class Meta:
        model = RoomReview
        fields = ['location', 'staff', 'cleanliness', 'value_for_money', 'comfort', 'facilities', 'free_wifi', 'name', 'email', 'comment']

        widgets = {
            'location': forms.Select(choices=STAR_CHOICES, attrs={'class': 'form-control'}),
            'staff': forms.Select(choices=STAR_CHOICES, attrs={'class': 'form-control'}),
            'cleanliness': forms.Select(choices=STAR_CHOICES, attrs={'class': 'form-control'}),
            'value_for_money': forms.Select(choices=STAR_CHOICES, attrs={'class': 'form-control'}),
            'comfort': forms.Select(choices=STAR_CHOICES, attrs={'class': 'form-control'}),
            'facilities': forms.Select(choices=STAR_CHOICES, attrs={'class': 'form-control'}),
            'free_wifi': forms.Select(choices=STAR_CHOICES, attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'required': 'true'}),
            'email': forms.EmailInput(attrs={'required': 'true'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'required': 'true'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'special_request']
        widgets = {
            'name': forms.TextInput(),
            'email': forms.EmailInput(),
            'phone': forms.NumberInput(),
            'special_request': forms.Textarea(attrs={'placeholder': 'Enter very detailed special request'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Your Message', 'rows': 4}),
        }

class FoodOrderForm(forms.ModelForm):
    class Meta:
        model = FoodOrder
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Full Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your Email Address', 'required': True}),
        }