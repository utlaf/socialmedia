# Generated by Django 4.2.4 on 2023-10-14 07:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0040_message_delete_chatmessage_delete_chatroom'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-date',)},
        ),
        migrations.RenameField(
            model_name='message',
            old_name='timestamp',
            new_name='date',
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('messages', models.ManyToManyField(blank=True, to='social.message')),
                ('participants', models.ManyToManyField(related_name='conversations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified',),
            },
        ),
    ]
