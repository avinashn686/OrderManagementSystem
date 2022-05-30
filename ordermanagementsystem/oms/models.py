import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, unique=True)
    password = models.CharField(max_length=50)
    user_type = models.CharField(max_length=255, null=True)
    ifLogged = models.BooleanField(default=False)
    def __str__(self):
        return "{} -{}".format(self.username, self.email)
@receiver(post_save, sender=User)
def user_created(instance, created, **kwargs):
    if created:
        instance_id = instance.id
        user_id = f'EM-{str(instance_id).zfill(3)}'
        instance.user_id = user_id
        instance.save()

class Product(models.Model):
    product_name = models.CharField(max_length=30)
    product_description = models.CharField(max_length=30, blank=True)
    product_id = models.CharField(max_length=255, null=True, blank=True)
    object_id = models.UUIDField(unique=True,editable=False,default=uuid.uuid4,
        verbose_name='Public identifier',
    )

@receiver(post_save, sender=Product)
def product_created(instance, created, **kwargs):
    if created:
        instance_id = instance.id
        product_id = f'PD-{str(instance_id).zfill(3)}'
        instance.product_id = product_id
        instance.save()


class Order(models.Model):
    product_id = models.ForeignKey(Product,related_name="%(app_label)s_%(class)s_product_id",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    user_id = models.ForeignKey(User,related_name="%(app_label)s_%(class)s_user_id",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    order_id = models.CharField(max_length=255, null=True, blank=True)
    object_id = models.UUIDField(unique=True,editable=False,default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    order_date = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Order)
def order_created(instance, created, **kwargs):
    if created:
        instance_id = instance.id
        order_id = f'OD-{str(instance_id).zfill(3)}'
        instance.order_id = order_id
        instance.save()
