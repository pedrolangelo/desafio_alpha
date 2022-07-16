# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from .models import Info


# @receiver(post_save, sender=Info)
# def create_or_update_periodic_task(sender, instance, created, **kwargs):
#     print("TESTE sinal")
#     if created:
#         instance.setup_task()
#     else:
#         if instance.task is not None:
#             instance.task.enabled = instance.status == Info.active
#             instance.task.save()


# @receiver(post_save, sender=Info)
# def set_or_sync_periodic_task(sender, instance=None, created=False, **kwargs):
#     if created:
#         instance.set_periodic_task(task_name='project_tasks')
#     else:
#         instance.sync_disable_enable_task(task_name='project_tasks')