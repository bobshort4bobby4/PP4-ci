from django import forms
from roombook.models import Booking


class AvailabilityForm(forms.Form):
    
    check_in = forms.DateField(required=True, widget=forms.DateTimeInput(attrs={'type': 'date'}))
    check_out = forms.DateField(required=True, widget=forms.DateTimeInput(attrs={'type': 'date'}))

    class Meta:
        fields = ['check_in', 'check_out']


class CancelConfirmForm(forms.Form):
    model = Booking

    
    class Meta:
        fields = ['user', 'room_number', 'check_in', 'check_out']

class ExtendBookingForm(forms.Form):
    check_out = forms.DateField(required=True, widget=forms.DateTimeInput(attrs={'type': 'date'}))
  

    class Meta:
        fields = ['check_out']
