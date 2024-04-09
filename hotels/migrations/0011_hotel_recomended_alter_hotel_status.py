# Generated by Django 5.0.3 on 2024-04-02 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0010_remove_room_is_booked'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='recomended',
            field=models.BooleanField(default=False, verbose_name='рекомендовать?'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='status',
            field=models.BooleanField(default=False, verbose_name='опубликовать?'),
        ),
    ]
