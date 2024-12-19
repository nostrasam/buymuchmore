from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser,CustomUserVerification
import secrets
from django.urls import reverse
from .tasks import *
from customer.models import Customer

# @receiver(post_save, sender=CustomUser)
# def verify_user(sender, instance, created, **kwargs):
#     if created:
#         token = secrets.token_hex(32)
#         CustomUserVerification.objects.create(
#             user=instance,
#             verification_token=token
#         )

#         verification_url = f'https://buymuchmore.com/mainauth/{reverse('verify', args=[token])}'
        
        
#         if instance.email:
#             user_register_send_email_task.delay(instance.email,verification_url)


@receiver(post_save,sender=CustomUserVerification)
def create_customer_profile(sender, created, instance, **kwargs):
    # Only trigger on updates, not creation
    if created:
            Customer.objects.create(user=instance)
            print(f"CustomerProfile created for user {instance.first_name}{instance.last_name}")

