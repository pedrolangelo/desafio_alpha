# Generated by Django 4.0.6 on 2022-07-15 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0016_alter_crontabschedule_timezone'),
        ('products', '0006_info_status_info_time_interval'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='task',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.periodictask'),
        ),
    ]