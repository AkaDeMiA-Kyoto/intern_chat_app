# Generated by Django 5.1 on 2024-09-25 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0029_talkroom_friend'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talkroom',
            name='friend',
        ),
    ]
