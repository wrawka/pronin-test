from django.core.cache import caches
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from service.models import Collection, Payment


@receiver(post_save, sender=Collection)
@receiver(post_delete, sender=Collection)
def invalidate_collection_cache(sender, instance, **kwargs):
    print(f"Invalidating cache for {sender.__name__} with ID {instance.id}")
    caches["api"].clear()


@receiver(post_save, sender=Payment)
@receiver(post_delete, sender=Payment)
def invalidate_payment_cache(sender, instance, **kwargs):
    print(f"Invalidating cache for {sender.__name__} with ID {instance.id}")
    caches["api"].clear()
