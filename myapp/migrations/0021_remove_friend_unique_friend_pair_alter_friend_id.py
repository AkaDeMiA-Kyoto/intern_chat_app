# Generated by Django 5.1 on 2024-09-23 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_alter_friend_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='friend',
            name='unique_friend_pair',
        ),
        migrations.AlterField(
            model_name='friend',
            name='id',
            field=models.CharField(editable=False, max_length=64, primary_key=True, serialize=False),
        ),
    ]
