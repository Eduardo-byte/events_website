# Generated by Django 3.2.8 on 2021-12-10 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20211210_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(blank=True, to='events.MyClubUser'),
        ),
        migrations.DeleteModel(
            name='EventUsers',
        ),
    ]
