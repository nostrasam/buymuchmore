from .models import AppInfo, Category, FeatureItem, Cart
from django.db.models import Sum

def slick(request):
    info = AppInfo.objects.get(pk=1)
    categ = Category.objects.all()
    categs = FeatureItem.objects.all()
    
    context = {
        'info':info,
        'categ':categ,
        'categs':categs,
    }
    
    return context



def cart_total_quantity(request):
    if request.user.is_authenticated:
        total_quantity = Cart.objects.filter(user=request.user, paid=False).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    else:
        total_quantity = 0
    return {'total_quantity': total_quantity}
