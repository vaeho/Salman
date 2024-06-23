from django import forms
from .models import Booking
from services.models import Service
from employees.models import Employee

class BookingForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.none())
    employee = forms.ModelChoiceField(queryset=Employee.objects.none())

    customer_first_name = forms.CharField(max_length=100)
    customer_last_name = forms.CharField(max_length=100)
    customer_phone_number = forms.CharField(max_length=20)

    class Meta:
        model = Booking
        fields = [
            'service', 'employee', 'customer_first_name', 'customer_last_name', 
            'customer_phone_number', 'date', 'time', 'total_amount'
        ]

    def __init__(self, *args, **kwargs):
        business = kwargs.pop('business', None)
        super().__init__(*args, **kwargs)
        if business:
            self.fields['service'].queryset = Service.objects.filter(business=business)
            self.fields['employee'].queryset = Employee.objects.filter(business=business)
