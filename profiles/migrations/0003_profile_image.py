# Generated by Django 2.2.2 on 2019-12-20 11:04

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name=profiles.models.images_path),
        ),
    ]