# Generated by Django 4.0.6 on 2022-07-15 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_info_remove_purchase_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=255),
        ),
        migrations.AddField(
            model_name='info',
            name='time_interval',
            field=models.CharField(choices=[('1 min', '1 min'), ('5 mins', '5 mins'), ('1 hour', '1 hour')], default='5 mins', max_length=255),
        ),
    ]
