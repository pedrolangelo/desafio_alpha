import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from celery.task.schedules import crontab

from django_celery_beat.models import IntervalSchedule, PeriodicTask

# Create your models here.

class Info(models.Model):
    active = 'Active'
    disabled = 'Disabled'

    one_min = '1 min'
    five_mins = '5 mins'
    one_hour = '1 hour'
    editar = 'editar'

    status = (
        (active, active),
        (disabled, disabled),
    )

    time_interval = (
        (one_min, one_min),
        (five_mins, five_mins),
        (one_hour, one_hour)
    )

    editar_time_interval = (
        (one_min, one_min),
        (five_mins, five_mins),
        (one_hour, one_hour),
        (editar, editar),
    )

    ativo = models.CharField(max_length=220)
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=220)
    inferior = models.FloatField()
    superior = models.FloatField()
    status = models.CharField(max_length=255, choices=status, default=active)
    time_interval = models.CharField(max_length=255, choices=time_interval, default=five_mins)
    editar_time_interval = models.CharField(max_length=255, choices=editar_time_interval, default=editar)


    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.ativo)


    def set_periodic_task(self, task_name):
        schedule = self.get_or_create_interval()
        PeriodicTask.objects.create(
            interval=schedule, 
            name=f'{self.ativo}-{self.id}', 
            task=task_name,
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )

    def get_or_create_interval(self):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=self.definir_tempo, period=self.definir_periodo
        )
        return schedule

    def get_periodic_task(self, task_name):
        interval = self.get_or_create_interval()
        periodic_task = PeriodicTask.objects.get(
            name=f'{self.ativo}-{self.id}', 
            task=task_name,
        )
        return periodic_task

    def sync_disable_enable_task(self, task_name):
        periodic_task = self.get_periodic_task(task_name)
        if(self.status == 'Active'):
            periodic_task.enabled = True
            periodic_task.save()
        if(self.status == 'Disabled'):
            periodic_task.enabled = False
            periodic_task.save()

    def sync_change_interval(self, task_name):
        if(self.editar_time_interval != 'editar'):
            periodic_task = self.get_periodic_task(task_name)

            schedule, created = IntervalSchedule.objects.get_or_create(
                every=self.definir_tempo_editar, period=self.definir_periodo_editar
            )

            self.sync_disable_enable_task(task_name='enviar_email')

            periodic_task.delete()

            PeriodicTask.objects.create(
            interval=schedule, 
            name=f'{self.ativo}-{self.id}', 
            task=task_name,
            args=json.dumps([self.id]),
            start_time=timezone.now()
            )

    @property
    def definir_tempo(self):
        if self.time_interval == '1 min':
            return '1'
        if self.time_interval == '5 mins':
            return '5'
        if self.time_interval == '1 hour':
            return '60'

        raise NotImplementedError(
            '''Interval Schedule for {interval} is not added.'''.format(
                interval=self.time_interval.value))

    @property
    def definir_periodo(self):
        if self.time_interval == '1 min':
            return 'minutes'
        if self.time_interval == '5 mins':
            return 'minutes'
        if self.time_interval == '1 hour':
            return 'minutes'

        raise NotImplementedError(
            '''Interval Schedule for {interval} is not added.'''.format(
                interval=self.time_interval.value))
    @property
    def definir_tempo_editar(self):
        if self.editar_time_interval == '1 min':
            return '1'
        if self.editar_time_interval == '5 mins':
            return '5'
        if self.editar_time_interval == '1 hour':
            return '60'

        raise NotImplementedError(
            '''Interval Schedule for {interval} is not added.'''.format(
                interval=self.time_interval.value))

    @property
    def definir_periodo_editar(self):
        if self.editar_time_interval == '1 min':
            return 'minutes'
        if self.editar_time_interval == '5 mins':
            return 'minutes'
        if self.editar_time_interval == '1 hour':
            return 'minutes'

        raise NotImplementedError(
            '''Interval Schedule for {interval} is not added.'''.format(
                interval=self.time_interval.value))

@receiver(post_save, sender=Info)
def set_or_sync_periodic_task(sender, instance, created, **kwargs):
    if created:
        instance.set_periodic_task(task_name='enviar_email')
    else:        
        instance.sync_change_interval(task_name='enviar_email')    
        instance.sync_disable_enable_task(task_name='enviar_email')