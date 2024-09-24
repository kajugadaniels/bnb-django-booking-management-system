from django import forms
from home.models import *

class RoomReviewForm(forms.ModelForm):
    class Meta:
        model = RoomReview
        fields = ['location', 'staff', 'cleanliness', 'value_for_money', 'comfort', 'facilities', 'free_wifi', 'name', 'email', 'comment']

        widgets = {
            'location': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'staff': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'cleanliness': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'value_for_money': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comfort': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'facilities': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'free_wifi': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment'}),
        }
