# Generated by Django 5.0.4 on 2025-06-25 12:25

import imagekit.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_alter_booking_options_foodorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='hero_desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='hero_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='settings/hero_images/'),
        ),
        migrations.AddField(
            model_name='setting',
            name='hero_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='about_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
