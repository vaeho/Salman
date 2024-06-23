from django.db import models
from core.models import BusinessUser
from employees.models import Employee

class Service(models.Model):
    business = models.ForeignKey(BusinessUser, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in minutes", default=30)
    employees = models.ManyToManyField(Employee, related_name='services')

    def __str__(self):
        return self.name