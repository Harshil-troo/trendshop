# Generated by Django 5.0.6 on 2024-05-24 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trendshop_website', '0004_alter_product_options_alter_category_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='product_images/default-product-image.jpg', upload_to='product_images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='product_images/default-product-image.jpg', upload_to='product_images/'),
        ),
    ]
