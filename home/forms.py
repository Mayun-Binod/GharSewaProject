from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['book_date', 'book_days', 'book_hours', 'status', 'customer', 'user', 'service']
