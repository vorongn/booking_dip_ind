# Generated by Django 5.0.3 on 2024-04-01 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_hotel_short_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_booked',
            field=models.BooleanField(default=False, verbose_name='Занят?'),
        ),
    ]