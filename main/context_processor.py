from .models import AppInfo, Category, FeatureItem

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