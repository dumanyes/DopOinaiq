from django import forms
from .models import TimeSlot
from .models import TurfReview

class BookingForm(forms.Form):
    timeslot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.filter(booked=False),
        empty_label="Select a Timeslot",
        label="Select Timeslot",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    user_name = forms.CharField(
        label="Your Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )



class ReviewForm(forms.ModelForm):
    class Meta:
        model = TurfReview
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.NumberInput(attrs={'type': 'number', 'min': '1', 'max': '5'}),
            'review_text': forms.Textarea(attrs={'rows': 4}),
        }
