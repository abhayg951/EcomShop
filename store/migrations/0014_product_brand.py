# Generated by Django 3.2.25 on 2024-07-26 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_product_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(default='No Brand', max_length=255),
        ),
    ]