# Generated by Django 4.1.2 on 2023-04-04 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_city_profile_college_id_profile_college_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(upload_to='profile'),
        ),
    ]
