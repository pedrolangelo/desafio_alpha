# Generated by Django 4.0.6 on 2022-07-13 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_name_product_ativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inferior',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='superior',
            field=models.PositiveBigIntegerField(default=2),
            preserve_default=False,
        ),
    ]
