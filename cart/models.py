from django.db import models
from mainauth.models import CustomUser
from product.models import Product
import uuid
# Create your models here.
   
class Cart(models.Model):
    cart_id = models.UUIDField(editable=False,unique=True,default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=30,choices=[('active','Active'),('checked_out','Checked Out')],default='active')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"({self.user.username})||{self.status}||{self.created_at}"  
        elif not self.user:
            return f"Anonymous User - {self.session_id}||{self.created_at}"
        
        def merge_items(self, anonymous_cart):
        
            # Merge items from another cart into this one (used during login).
            for items in anonymous_cart.cart_cartitems.all():
                cart_item, created = CartItems.objects.get_or_create(cart=self, product=items.product)
                if not created:
                    cart_item.quantity += items.quantity
                cart_item.save()

            anonymous_cart.delete()

    
class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='cart_cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name = 'product_cartitem')  # Correct reference to Product model
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart
    subtotal_price = models.CharField(max_length=50)  # You can calculate total amount dynamically if needed

    class Meta:
        unique_together = ('cart', 'product')  # Ensure no duplicate products in the same cart

    def save(self,*args, **kwargs):
        self.subtotal_price = self.price * self.quantity
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.cart}"