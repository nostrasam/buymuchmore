# Generated by Django 5.0.4 on 2024-10-26 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_product_unpaid_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unpaid_count',
            field=models.IntegerField(),
        ),
    ]
