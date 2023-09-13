# Generated by Django 4.2.1 on 2023-09-13 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_delete_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk_content',
            name='user_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='talk_content',
            name='user_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
