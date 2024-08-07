# Generated by Django 5.0.4 on 2024-07-06 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_customer_latitude_customer_longitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='longitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='longitude',
            field=models.FloatField(),
        ),
    ]
