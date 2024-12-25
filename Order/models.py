from django.db import models
from cart.models import *
from mainauth.models import CustomUser
from product.models import Product
import uuid


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,
                              choices=[
                                  ('pending','Pending'),
                                  ('completed','Completed'),
                                  ('cancelled','Cancelled')
                              ],
                              default='pending'
                              )
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    reference_id = models.UUIDField(editable=False,default=uuid.uuid4(),unique=True)


    def __str__(self):
        return f"{self.user.first_name}||{self.reference_id}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='orderitem_products')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)

    def save(self,*args, **kwargs):
        self.subtotal_price = self.price * self.quantity
        super().save(*args,**kwargs)


    def __str__(self):
        return f"{self.order.user.first_name}||{self.product}"



