# Generated by Django 5.0.4 on 2024-07-21 06:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('male', 'MALE'), ('children', 'CHILDREN'), ('female', 'FEMALE')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='is_featured',
            field=models.BooleanField(default=False, null=True),
        ),
    ]