# Generated by Django 5.0.6 on 2024-06-22 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_businessuser_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
