# Generated by Django 3.0.1 on 2019-12-25 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='back_side_image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='final_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='initial_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='left_side_image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='main_image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='right_side_image',
        ),
    ]
