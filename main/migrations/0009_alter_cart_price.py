# Generated by Django 5.0.4 on 2024-10-10 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_payment_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
