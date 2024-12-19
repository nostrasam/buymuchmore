from django.db import models
from mainauth.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=20,choices=
                            [
                              ('review','Review'),
                              ('rating', 'Rating'),
                              ('payment','Payment'),
                              ('callback_request','Callback_Request'),
                              ('order', 'Order'),
                            ])
    message = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type','object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(null=True,blank=True)

