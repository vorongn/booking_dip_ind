# Generated by Django 5.0.3 on 2024-04-07 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0016_room_baths_alter_hotel_short_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='bads',
            field=models.IntegerField(default=False, verbose_name='кроватей'),
        ),
    ]