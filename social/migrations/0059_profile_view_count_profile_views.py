# Generated by Django 4.2.4 on 2023-10-24 08:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0058_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='viewed_profiles', to=settings.AUTH_USER_MODEL),
        ),
    ]
