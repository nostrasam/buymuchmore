# Generated by Django 5.0.4 on 2024-10-26 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_product_is_vat_exempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unpaid_count',
            field=models.IntegerField(default=0),
        ),
    ]
