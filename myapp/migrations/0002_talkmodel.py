# Generated by Django 3.1 on 2022-02-19 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TalkModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('talkname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talkname', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pub_date',),
            },
        ),
    ]
