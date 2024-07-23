# Generated by Django 5.0.4 on 2024-07-22 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_options_category_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('Children', 'Children'), ('Women', 'Women'), ('Men', 'Men')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
