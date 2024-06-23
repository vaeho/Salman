# employees/forms.py
from django import forms
from .models import Employee
from services.models import Service

class EmployeeAddForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500'})
    )

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phone_number', 'role', 'services']

    def __init__(self, *args, **kwargs):
        self.business = kwargs.pop('business', None)
        super().__init__(*args, **kwargs)
        if self.business:
            self.fields['services'].queryset = Service.objects.filter(business=self.business)