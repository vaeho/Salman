# Generated by Django 5.0.6 on 2024-06-23 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_service_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='business',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='business',
        ),
        migrations.RemoveField(
            model_name='service',
            name='employees',
        ),
        migrations.RemoveField(
            model_name='service',
            name='business',
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]
