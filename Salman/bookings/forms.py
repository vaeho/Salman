# bookings/forms.py
from django import forms
from .models import Booking
from services.models import Service
from employees.models import Employee

class BookingForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.none(), label="Services")
    employee = forms.ModelChoiceField(queryset=Employee.objects.none(), label="Employee")
    customer_first_name = forms.CharField(max_length=100, label="First Name")
    customer_last_name = forms.CharField(max_length=100, label="Last Name")
    customer_phone_number = forms.CharField(max_length=20, label="Phone Number")
    customer_email = forms.EmailField(required=False, label="Email (Optional)")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    total_amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Booking
        fields = [
            'services', 'employee', 'customer_first_name', 'customer_last_name',
            'customer_phone_number', 'customer_email', 'date', 'time', 'total_amount'
        ]

    def __init__(self, *args, **kwargs):
        business = kwargs.pop('business', None)
        super().__init__(*args, **kwargs)
        if business:
            self.fields['services'].queryset = Service.objects.filter(business=business)
            self.fields['employee'].queryset = Employee.objects.filter(business=business)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-input'})

    def clean(self):
        cleaned_data = super().clean()
        services = cleaned_data.get('services')
        if not services:
            raise forms.ValidationError("At least one service must be selected.")
        return cleaned_data