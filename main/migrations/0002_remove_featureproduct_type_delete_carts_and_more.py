# Generated by Django 5.0.4 on 2024-05-06 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featureproduct',
            name='type',
        ),
        migrations.DeleteModel(
            name='Carts',
        ),
        migrations.DeleteModel(
            name='FeatureProduct',
        ),
    ]