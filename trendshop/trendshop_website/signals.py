from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def post_save_order(instance, *args, **kwargs):
    order_id = "{}{:04d}".format('ORD', instance.id)
    instance.cart.status = False
    instance.cart.save()
    Order.objects.filter(id=instance.id).update(order=order_id)
    return instance
