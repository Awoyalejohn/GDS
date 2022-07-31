from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderlineItem

@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order subtotal on lineitem update/create
    """
    instance.order.update_subtotal()

@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order subtotal on lineitem delete
    """
    print('delete signal received')
    instance.order.update_subtotal()
