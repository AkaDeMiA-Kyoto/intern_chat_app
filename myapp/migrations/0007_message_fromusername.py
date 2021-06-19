# Generated by Django 3.1 on 2021-05-21 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0006_auto_20210522_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='fromusername',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from1', to=settings.AUTH_USER_MODEL),
        ),
    ]
