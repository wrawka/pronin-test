from django.core.cache import caches
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from service.models import Collection, Payment
from service.tasks import send_collection_created_email, send_payment_created_email


@receiver(post_save, sender=Collection)
@receiver(post_delete, sender=Collection)
def invalidate_collection_cache(sender, instance, **kwargs):
    caches["api"].clear()


@receiver(post_save, sender=Payment)
@receiver(post_delete, sender=Payment)
def invalidate_payment_cache(sender, instance, **kwargs):
    caches["api"].clear()


@receiver(post_save, sender=Collection)
def collection_created_handler(sender, instance, created, **kwargs):
    if created:
        send_collection_created_email.delay(instance.id)


@receiver(post_save, sender=Payment)
def payment_created_handler(sender, instance, created, **kwargs):
    if created:
        send_payment_created_email.delay(instance.id)
