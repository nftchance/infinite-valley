# Generated by Django 5.0 on 2023-12-05 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('day', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='image_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]
