# Generated by Django 5.0.3 on 2024-04-09 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0027_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(default=1, verbose_name='рейтинг'),
            preserve_default=False,
        ),
    ]
