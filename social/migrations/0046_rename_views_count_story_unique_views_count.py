# Generated by Django 4.2.4 on 2023-10-15 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0045_story_views_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='views_count',
            new_name='unique_views_count',
        ),
    ]