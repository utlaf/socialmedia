# Generated by Django 4.2.4 on 2023-10-05 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0018_profile_date_modified_delete_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]