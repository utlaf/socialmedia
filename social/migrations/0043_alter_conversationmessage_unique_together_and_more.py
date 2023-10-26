# Generated by Django 4.2.4 on 2023-10-15 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0042_alter_conversation_options_alter_message_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='conversationmessage',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='conversationmessage',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='conversationmessage',
            name='message',
        ),
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.DeleteModel(
            name='ConversationMessage',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]