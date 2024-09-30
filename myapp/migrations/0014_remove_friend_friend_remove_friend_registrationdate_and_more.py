# Generated by Django 5.1 on 2024-09-14 14:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_alter_customuser_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='friend',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='registrationDate',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='talkDate',
        ),
        migrations.AlterField(
            model_name='friend',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Frienduser', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registrationDate', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('talkDate', models.DateTimeField(auto_now=True, verbose_name='会話日時')),
                ('message', models.TextField()),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.friend')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='friend',
            name='friends',
            field=models.ManyToManyField(through='myapp.Friendship', to=settings.AUTH_USER_MODEL, verbose_name='友達'),
        ),
    ]
