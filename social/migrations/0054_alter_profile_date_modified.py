# Generated by Django 4.2.4 on 2023-10-22 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0053_remove_profile_is_online_profile_last_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_modified',
            field=models.DateField(auto_now=True),
        ),
    ]
