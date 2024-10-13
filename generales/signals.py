from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from generales.models import Project


@receiver(post_save, sender=Project)
@receiver(post_delete, sender=Project)
def clear_project_list_cache(sender, **kwargs):
    cache_key = 'project_list'
    cache.delete(cache_key)
