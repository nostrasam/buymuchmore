# Generated by Django 5.0.4 on 2024-09-23 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_cart_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(max_length=20),
        ),
    ]