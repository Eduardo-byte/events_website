# Generated by Django 3.2.8 on 2021-12-09 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_myclubuser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myclubuser',
            name='user',
        ),
    ]