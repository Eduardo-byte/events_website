# Generated by Django 3.2.8 on 2023-03-10 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_alter_event_venue'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='venus_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]