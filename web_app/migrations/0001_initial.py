# Generated by Django 4.2.8 on 2023-12-26 15:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number_code', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=12)),
                ('country', models.CharField(max_length=100)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('cardholder_name', models.CharField(max_length=255)),
                ('expiration_date', models.CharField(max_length=5)),
                ('card_type', models.CharField(choices=[('VISA', 'Visa'), ('MC', 'Mastercard')], max_length=4)),
                ('cvc', models.CharField(max_length=4)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tokens', models.JSONField(default=list, null=True)),
                ('username', models.CharField(max_length=25, unique=True, validators=[django.core.validators.MinLengthValidator(4, 'Usernames must be between 4 and 25 characters.')])),
                ('password', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('avatar', models.CharField(max_length=255, null=True)),
                ('account_type', models.CharField(choices=[('V', 'Vendor'), ('C', 'Customer')], max_length=1)),
                ('cart_quantity', models.IntegerField(default=0)),
                ('addresses', models.ManyToManyField(to='web_app.address')),
                ('cards', models.ManyToManyField(to='web_app.card')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('images', models.JSONField(default=list, null=True)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(max_length=255, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.FloatField()),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Delivered'), ('C', 'Canceled')], default='A', max_length=1)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web_app.address')),
                ('card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web_app.card')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web_app.user')),
                ('products', models.ManyToManyField(to='web_app.cartproduct')),
            ],
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.product'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.user')),
                ('products', models.ManyToManyField(to='web_app.cartproduct')),
            ],
        ),
    ]
