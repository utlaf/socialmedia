# Generated by Django 4.2.4 on 2023-10-06 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0027_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
