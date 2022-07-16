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

    status = (
        (active, active),
        (disabled, disabled),
    )

    time_interval = (
        (one_min, one_min),
        (five_mins, five_mins),
        (one_hour, one_hour)
    )

    ativo = models.CharField(max_length=220)
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=220)
    inferior = models.FloatField()
    superior = models.FloatField()
    status = models.CharField(max_length=255, choices=status, default=active)
    time_interval = models.CharField(max_length=255, choices=time_interval, default=five_mins)

    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.ativo)

    def setup_task(self):
        print("Criei tarefa")
        self.task = PeriodicTask.objects.create(
            name=self.ativo,
            task='enviar_email',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )
        self.save()

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
            every=1, period='minutes'
        )
        return schedule

    def get_periodic_task(self, task_name):
        interval = self.get_or_create_interval()
        periodic_task = PeriodicTask.objects.get(
            interval=interval, 
            name=f'{self.ativo}-{self.id}', 
            task=task_name,
        )
        return periodic_task

    def sync_disable_enable_task(self, task_name):
        periodic_task = self.get_periodic_task(task_name)
        periodic_task.enabled = self.status
        periodic_task.save()

    @property
    def interval_schedule(self):
        print("ENTREI NO interval_schedule")
        one_min = '1 min'
        five_mins = '5 mins'
        one_hour = '1 hour'
        time_interval = (
            (one_min, one_min),
            (five_mins, five_mins),
            (one_hour, one_hour)
        )
        if self.time_interval == '1 min':
            print("ENTREI NO 1MIN")
            return IntervalSchedule.objects.get(every=1, period='minutes')
        if self.time_interval == '5 mins':
            print("ENTREI NO 5MIN")
            return IntervalSchedule.objects.get(every=5, period='minutes')
        if self.time_interval == '1 hour':
            print("ENTREI NO 1HOUR")
            return IntervalSchedule.objects.get(every=1, period='hours')

        raise NotImplementedError(
            '''Interval Schedule for {interval} is not added.'''.format(
                interval=self.time_interval.value))

@receiver(post_save, sender=Info)
def set_or_sync_periodic_task(sender, instance, created, **kwargs):
    if created:
        print("CRIADA")
        instance.set_periodic_task(task_name='enviar_email')
    else:        
        if Info.status == 'Disabled':
            task = PeriodicTask.objects.get(Info.id) 
            task.enabled = False 
            task.save()