# Generated by Django 5.0.3 on 2024-04-01 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0007_hotel_logo_hotel'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='short_desc',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]