# Generated by Django 4.1.2 on 2023-04-04 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_coupon_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_quality',
            field=models.IntegerField(default=0),
        ),
    ]