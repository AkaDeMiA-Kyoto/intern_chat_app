# Generated by Django 3.1 on 2021-11-21 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='intern/myapp/static/myapp/img/defaultuser.png', upload_to='userimg/'),
        ),
    ]
