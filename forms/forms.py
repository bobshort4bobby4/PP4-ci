from django import forms


class AvailabilityForm(forms.Form):
    
    check_in = forms.DateField(required=True, widget=forms.DateTimeInput(attrs={'type': 'date'}))
    check_out = forms.DateField(required=True, widget=forms.DateTimeInput(attrs={'type': 'date'}))

    class Meta:
        fields = ['check_in', 'check_out']