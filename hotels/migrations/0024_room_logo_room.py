# Generated by Django 5.0.3 on 2024-04-08 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0023_alter_booking_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='logo_room',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/rooms/logo/', verbose_name='главное фото номера'),
        ),
    ]
