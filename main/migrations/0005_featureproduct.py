# Generated by Django 5.0.4 on 2024-06-04 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_subscription_subscribe'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('condition', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('availability', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('postcode', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.IntegerField()),
                ('promo_price', models.IntegerField(blank=True, null=True)),
                ('telephone1', models.CharField(max_length=50)),
                ('telephone2', models.CharField(blank=True, max_length=50, null=True)),
                ('seller_name', models.CharField(max_length=100)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('carimg', models.ImageField(upload_to='carimg')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.featureitem')),
            ],
        ),
    ]