# Generated by Django 5.1.4 on 2025-01-04 16:33

import location.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_location_postal_code_alter_location_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='coordinates',
            field=models.JSONField(blank=True, default=location.models.get_default_coordinates, help_text='Coordinates in {lat: float, lng: float} format', null=True),
        ),
    ]
