# Generated by Django 3.1 on 2021-11-21 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20211121_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='userimg/defaultuser.png', upload_to='userimg/'),
        ),
    ]
