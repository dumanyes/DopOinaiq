from django import forms
from .models import ProductReview


class YourOrderForm(forms.Form):
    shipping_address = forms.CharField(
        label='Shipping Address',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your shipping address'}),
        required=True,  # Use `required=True` instead of `required=True,`
    )
    payment_method = forms.ChoiceField(
        label='Payment Method',
        choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')],
        widget=forms.RadioSelect,
        required=True,
    )
    # Add more fields as needed for your order form

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.NumberInput(attrs={'type': 'number', 'min': '1', 'max': '5'}),
            'review_text': forms.Textarea(attrs={'rows': 4}),
        }