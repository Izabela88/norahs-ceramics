# Generated by Django 4.0.4 on 2022-06-15 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_addressdetails_user_phone_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addressdetails',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='addressdetails',
            name='longitude',
        ),
    ]
