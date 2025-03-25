# Generated by Django 5.1.4 on 2025-03-25 06:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0002_alter_listing_location'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listing',
            options={'ordering': ['title'], 'verbose_name_plural': '3. Annonces'},
        ),
        migrations.AddField(
            model_name='listing',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
