# Generated by Django 4.1.4 on 2023-10-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0060_remove_profile_view_count_remove_profile_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]