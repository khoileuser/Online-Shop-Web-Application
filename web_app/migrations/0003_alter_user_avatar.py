# Generated by Django 4.2.7 on 2023-12-06 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0002_user_cart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
