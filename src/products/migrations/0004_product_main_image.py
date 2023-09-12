# Generated by Django 3.0.1 on 2019-12-25 14:26

from django.db import migrations, models
import products.utils


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20191225_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to=products.utils.upload_image_path),
        ),
    ]
