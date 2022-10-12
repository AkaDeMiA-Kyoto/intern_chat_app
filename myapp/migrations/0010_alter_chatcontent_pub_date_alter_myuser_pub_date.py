# Generated by Django 4.0.4 on 2022-10-12 16:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_chatcontent_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatcontent',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date sent'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時'),
        ),
    ]
