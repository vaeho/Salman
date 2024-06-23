from django.db import models
from core.models import BusinessUser
# Create your models here.

class Employee(models.Model):
    business = models.ForeignKey(BusinessUser, on_delete=models.CASCADE, related_name='employees')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
