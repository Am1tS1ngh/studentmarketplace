# Generated by Django 4.1.2 on 2023-03-04 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_colorvariant_sizevariant_product_color_variant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color_Variant',
            field=models.ManyToManyField(blank=True, to='products.colorvariant'),
        ),
        migrations.AlterField(
            model_name='product',
            name='size_Variant',
            field=models.ManyToManyField(blank=True, to='products.sizevariant'),
        ),
    ]
