# Generated by Django 4.2.4 on 2023-10-12 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0035_chat_chatmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='user',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
    ]
