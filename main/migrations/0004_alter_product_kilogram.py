# Generated by Django 5.0.4 on 2024-09-23 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product_kilogram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='kilogram',
            field=models.FloatField(),
        ),
    ]
