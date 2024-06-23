from django.db import models
from core.models import BusinessUser
from services.models import Service
from employees.models import Employee
from customers.models import Customer
# Create your models here.

class Booking(models.Model):
    business = models.ForeignKey(BusinessUser, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.service.name} Booking'

    def save(self, *args, **kwargs):
        # Create or update customer based on phone number
        customer, created = Customer.objects.update_or_create(
            phone_number=self.customer.phone_number,
            defaults={
                'first_name': self.customer.first_name,
                'last_name': self.customer.last_name,
                'email': self.customer.email,
                'business': self.business,
            }
        )
        self.customer = customer
        super().save(*args, **kwargs)
