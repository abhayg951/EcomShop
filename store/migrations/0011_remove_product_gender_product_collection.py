# Generated by Django 5.0.4 on 2024-07-22 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_product_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='gender',
        ),
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.CharField(choices=[('Men', 'Men'), ('Women', 'Women'), ('Children', 'Children')], max_length=10, null=True),
        ),
    ]
