# Generated by Django 5.1.4 on 2025-01-04 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0007_listing_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customtag',
            name='category',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='business_hours',
        ),
        migrations.CreateModel(
            name='BusinessHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday_open', models.TimeField(blank=True, null=True)),
                ('monday_close', models.TimeField(blank=True, null=True)),
                ('monday_closed', models.BooleanField(default=False)),
                ('tuesday_open', models.TimeField(blank=True, null=True)),
                ('tuesday_close', models.TimeField(blank=True, null=True)),
                ('tuesday_closed', models.BooleanField(default=False)),
                ('wednesday_open', models.TimeField(blank=True, null=True)),
                ('wednesday_close', models.TimeField(blank=True, null=True)),
                ('wednesday_closed', models.BooleanField(default=False)),
                ('thursday_open', models.TimeField(blank=True, null=True)),
                ('thursday_close', models.TimeField(blank=True, null=True)),
                ('thursday_closed', models.BooleanField(default=False)),
                ('friday_open', models.TimeField(blank=True, null=True)),
                ('friday_close', models.TimeField(blank=True, null=True)),
                ('friday_closed', models.BooleanField(default=False)),
                ('saturday_open', models.TimeField(blank=True, null=True)),
                ('saturday_close', models.TimeField(blank=True, null=True)),
                ('saturday_closed', models.BooleanField(default=False)),
                ('sunday_open', models.TimeField(blank=True, null=True)),
                ('sunday_close', models.TimeField(blank=True, null=True)),
                ('sunday_closed', models.BooleanField(default=False)),
                ('listing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='operating_hours', to='listing.listing')),
            ],
        ),
    ]
