# Generated by Django 5.0.4 on 2024-09-23 05:45

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appname', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='logo')),
                ('carousel1', models.ImageField(upload_to='carousel')),
                ('carousel2', models.ImageField(upload_to='carousel')),
                ('carousel3', models.ImageField(upload_to='carousel')),
                ('banner', models.ImageField(upload_to='banner')),
                ('copyright', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('pix', models.ImageField(upload_to='pix')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('email', models.EmailField(max_length=100)),
                ('telephone', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('sent', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('sponsorname', models.CharField(default='a', max_length=50)),
                ('website', models.URLField(default='a')),
                ('pix', models.ImageField(upload_to='pix')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('pix', models.ImageField(upload_to='pix')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=50)),
                ('pix', models.ImageField(upload_to='customer')),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
                ('availability', models.CharField(default='a', max_length=50)),
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
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('company_name', models.CharField(blank=True, max_length=50, null=True)),
                ('company_registration', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=150)),
                ('address_type', models.CharField(choices=[('seller', 'Seller Address'), ('delivery', 'Delivery Service Address')], default='seller', max_length=8)),
                ('phone', models.CharField(max_length=50)),
                ('postcode', models.CharField(blank=True, max_length=100, null=True)),
                ('coverage_zones', models.CharField(blank=True, max_length=50, null=True)),
                ('delivery_services', models.CharField(blank=True, max_length=150, null=True)),
                ('operating_hours', models.IntegerField(blank=True, null=True)),
                ('service_rates', models.IntegerField(blank=True, null=True)),
                ('vehicle_types', models.CharField(blank=True, max_length=100, null=True)),
                ('availability', models.CharField(default='a', max_length=50)),
                ('business_sector', models.CharField(choices=[('Logistics', 'Logistics'), ('Insurance', 'Insurance'), ('Agriculture', 'Agriculture'), ('Manufacturing', 'Manufacturing'), ('Trading', 'Trading')], default='a', max_length=50)),
                ('pix', models.ImageField(upload_to='merchant')),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('amount', models.IntegerField()),
                ('paid', models.BooleanField()),
                ('phone', models.CharField(max_length=50)),
                ('pay_code', models.CharField(max_length=50)),
                ('additional_info', models.TextField()),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('condition', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('availability', models.CharField(default='a', max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('postcode', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.FloatField()),
                ('promo_price', models.IntegerField(blank=True, null=True)),
                ('telephone1', models.CharField(max_length=50)),
                ('telephone2', models.CharField(blank=True, max_length=50, null=True)),
                ('seller_name', models.CharField(max_length=100)),
                ('website', models.CharField(blank=True, max_length=50, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('carimg', models.ImageField(upload_to='carimg')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rating_value', models.FloatField(default=0.0)),
                ('rating_count', models.PositiveIntegerField(default=0)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('paid', models.BooleanField()),
                ('amount', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('promo_price', models.IntegerField(blank=True, null=True)),
                ('subcribeimg', models.ImageField(upload_to='subcribeimg')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subscription')),
            ],
        ),
        migrations.CreateModel(
            name='ProductRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
    ]
