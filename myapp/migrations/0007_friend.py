# Generated by Django 5.1 on 2024-09-13 22:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_customuser_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registrationDate', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('friendName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Friend', to=settings.AUTH_USER_MODEL, verbose_name='友達')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Frienduser', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
    ]
