import uuid
import json
import requests


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.core.mail import EmailMessage 
from django.db.models import Q
from main.models import *
from .forms import *
from .models import Customer, Product, FeatureProduct, Review, Cart
from django.db.models import Sum


from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

# Create your views here.
    

def home(request):
    categ = Category.objects.all()
    categs = FeatureItem.objects.all()
    
    context = {
       'categ':categ,
       'categs':categs,
          
    }
    
    return render(request, 'index.html', context)
    

def category(request, id, slug):
    merchant_brand = Category.objects.get(pk=id)
    merchant_item = Product.objects.filter(type_id = id)

    context = {
        'merchant_brand':merchant_brand,
        'merchant_item':merchant_item,
    }
    
    return render(request, 'category.html', context)


def featureitem(request, id, slug):
    merchant1_brand = FeatureItem.objects.get(pk=id)
    merchant1_item = Product.objects.filter(type_id = id)

    context = {
        'merchant1_brand':merchant1_brand,
        'merchant1_item':merchant1_item,
    }
    
    return render(request, 'featureitem.html', context)


def products(request):
    products = Product.objects.all()
    reviews = Review.objects.all()  # Assuming you have a queryset for all reviews
    p = Paginator(products, 12)
    page = request.GET.get('page')
    pagin = p.get_page(page)
    
    context = {
        'pagin': pagin,
        'reviews': reviews,  # Pass the reviews queryset to the template
    }
    
    return render(request, 'products.html', context)

def subscription_products(request):
    products = Subscribe.objects.all()
    p = Paginator(products, 8)
    page = request.GET.get('page')
    pagin = p.get_page(page)
    
    context = {
        'pagin': pagin,
    }
    
    return render(request, 'subscription_products.html', context)


def detail(request, id, slug):
    merchant_det = Product.objects.get(pk=id)
    
    context ={
        'merchant_det':merchant_det,
    }
    
    return render(request, 'detail.html', context)

def featuredetail(request, id, slug):
    merchant_det1 = Product.objects.get(pk=id)
    
    context ={
        'merchant_det1':merchant_det1,
    }
    
    return render(request, 'featuredetail.html', context)

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "your message has been sent successfully!!!")
            return redirect('home')
        
    context = {
        'form':form,
    }
        
    return render(request, 'contact.html', context)


def signout(request):
    logout(request)
    messages.success(request, 'you are now signed out')
    return redirect('signin')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'login successfully!')
            return redirect('home')
        else:
            messages.error(request, 'username/password is incorrect please try again')
            return redirect('signin')
        
    return render(request, 'login.html')

def merchsignin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'login successfully!')
            return redirect('home')
        else:
            messages.error(request, 'username/password is incorrect please try again')
            return redirect('merchsignin')
        
    return render(request, 'logins.html')


def register(request):
    form = CustomerForm()  # Renamed variable to avoid naming conflict

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user instance
            address = request.POST['address']
            phone = request.POST['phone']
            pix = request.POST['pix']

            # Create and save Customer object
            new_customer = Customer(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=phone,
                address=address,
                pix=pix
            )
            new_customer.save()

            messages.success(request, f'Dear {user.username}, your account is successfully created')
            return redirect('signin')
        else:
            # Pass form errors to the template for display
            messages.error(request, form.errors)

    return render(request, 'register.html', {'form': form})

def merchregistration(request):
    form = MerchantForm()  # Renamed variable to avoid naming conflict

    if request.method == 'POST':
        form = MerchantForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user instance
            address = request.POST['address']
            phone = request.POST['phone']
            pix = request.POST['pix']
            company_name = request.POST['company_name']
            company_registration = request.POST['company_registration']

            # Create and save Customer object
            new_merchant = Merchant(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=phone,
                company_name=company_name,
                company_registration=company_registration,
                address=address,
                pix=pix
            )
            new_merchant.save()

            messages.success(request, f'Dear {user.username}, your account is successfully created')
            return redirect('merchsignin')
        else:
            # Pass form errors to the template for display
            messages.error(request, form.errors)

    return render(request, 'merchregistration.html', {'form': form})

            
@login_required(login_url='signin')
def profile(request):
    userprof = Customer.objects.get(user__username=request.user.username)

    context = {
        'userprof': userprof
    }

    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def merchprofile(request):
    userprof = Merchant.objects.get(user__username=request.user.username)

    context = {
        'userprof': userprof
    }

    return render(request, 'merchprofile.html', context)


def profile_update(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    pform = ProfileForm(instance=request.user.customer)
    if request.method == 'POST':
        pform = ProfileForm(request.POST, request.FILES, instance=request.user.customer)
        if pform.is_valid():
            user = pform.save()
            new = user.first_name.title()
            messages.success(request, f"dear {new} your profile has been updated successfully!")
            return redirect('profile')
        else:
            new = user.first_name.title()
            messages.error(request, f'dear {new} your profile update generated the follow error: {pform.errors}')
            return redirect('profile_update')
        
    context = {
        'userprof':userprof
    }
    
    return render(request, 'profile_update.html', context)


def mechkyc_upload(request):
    userprof = Merchant.objects.get(user__username = request.user.username)
    pform = MerchantProfileForm(instance=request.user.merchant)
    if request.method == 'POST':
        pform = MerchantProfileForm(request.POST, request.FILES, instance=request.user.merchant)
        if pform.is_valid():
            user = pform.save()
            new = user.first_name.title()
            messages.success(request, f"dear {new} your document has been uploaded successfully. Please make your subscription payment and wait for 24 to 48 hours for account validation as a merchant!")
            return redirect('mechkyc_upload')
        else:
            new = user.first_name.title()
            messages.error(request, f'dear {new} your document upload generated the follow error: {pform.errors}')
            return redirect('mechkyc_upload')
        
    context = {
        'userprof':userprof
    }
    
    return render(request, 'mechkyc_upload.html', context)


@login_required(login_url='signin')
def password_update(request):
    userprof = Customer.objects.get(user__username=request.user.username)
    form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            new = request.user.username.title()
            messages.success(request, f"Dear {new}, your password has been updated!")
            return redirect('home')
        else:
            new = request.user.username.title()
            messages.error(request, f"Dear {new}, there is an error trying to change your password: {form.errors}")
            # Render the same template with the form and errors instead of redirecting
            return render(request, 'password_upda.html', {'userprof': userprof, 'form': form})

    context = {
        'userprof': userprof,
        'form': form
    }

    return render(request, 'password_update.html', context)

@login_required(login_url='signin')
def add_to_cart(request):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        itemsid = request.POST['itemsid']
        main = Product.objects.get(pk=itemsid)
        cart = Cart.objects.filter(user__username=request.user.username, paid=False)
        if cart.exists():
            basket = cart.filter(items=main, quantity=quantity).first()
            if basket:
                basket.quantity += quantity
                basket.amount = main.price * basket.quantity
                basket.save()
                messages.success(request, 'One item added to cart')
            else:
                newitem = Cart(user=request.user, items=main, quantity=quantity, price=main.price, amount=str(main.price * quantity), paid=False)
                newitem.save()
                messages.success(request, 'One item added to cart')
        else:
            newcart = Cart(user=request.user, items=main, quantity=quantity, price=main.price, amount=str(main.price * quantity), paid=False)
            newcart.save()
            messages.success(request, 'One item added to cart')

    # Calculate total items in the cart
    total_items_in_cart = Cart.objects.filter(user=request.user, paid=False).count()

    return redirect('products')

# Now, in the template where you display the cart icon, you can access the total_items_in_cart variable

@login_required(login_url='signin')       
def cart(request):
    cart_items = Cart.objects.filter(user__username=request.user.username, paid=False)

    # Calculate total quantity of items in the cart
    total_quantity = cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    for item in cart_items:
        item.amount = item.price * item.quantity
        item.save()
        
    subtotal = sum(item.price * item.quantity for item in cart_items)
    vat = 0.075 * subtotal
    total = subtotal + vat
        
    context = {
        'cart': cart_items,
        'subtotal': subtotal,
        'vat': vat,
        'total': total,
        'total_quantity': total_quantity  # Add total quantity to the context
    }
    
    return render(request, 'cart.html', context)


@login_required(login_url='signin')
def delete(request):
    if request.method == 'POST':
        del_item = request.POST['delid']
        Cart.objects.filter(pk=del_item).delete()
        messages.success(request, 'one item deleted')
        return redirect('cart')

@login_required(login_url='signin')   
def update(request):
    if request.method == 'POST':
        qty_item = request.POST['quantid']
        new_qty = request.POST['quant']
        newqty = Cart.objects.get(pk=qty_item)
        newqty.quantity = new_qty
        newqty.amount = newqty.price * newqty.quantity
        newqty.save()
        messages.success(request, 'quantity updated')
        return redirect('cart')
    
    
@login_required(login_url='signin')
def checkout(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    cart = Cart.objects.filter(user__username = request.user.username, paid=False)
    for item in cart:
        item.amount = item.price * item.quantity
        item.save()
        
    subtotal = 0
    vat = 0
    total = 0
    
    for item in cart:
        subtotal += item.price * item.quantity
        vat = 0.075 * subtotal
        total = subtotal + vat
        
    context = {
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
        'userprof':userprof
    }
    
    return render(request, 'checkout.html', context)


@login_required(login_url='signin')
def pay(request):
    if request.method == 'POST':
        api_key = 'sk_test_ddafcabdaed050c9422c8365430f1c50b79f83f1'  # Secret key from paystack
        curl = 'https://api.paystack.co/transaction/initialize'  # Paystack call url
        cburl = 'http://52.90.126.143/callback'  # Payment thank you page
        ref = str(uuid.uuid4())  # Reference number required by paystack as an additional order number
        profile = Customer.objects.get(user__username=request.user.username)
        order_no = profile.id  # Main order number
        total = float(request.POST['total']) * 100  # Total amount to be charged from customer card
        user = User.objects.get(username=request.user.username)  # Query the user model for customer details
        email = user.email  # Store customer to send to paystack
        first_name = request.POST['first_name']  # Collect from the template in case there is no change
        last_name = request.POST['last_name']  # Collect from the template in case there is no change
        phone = request.POST['phone']  # Collect from the template in case there is no change
        add_info = request.POST['add_info']  # Collect from the template in case there is no change

        # Collect data to send to paystack via call
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference': ref, 'amount': int(total), 'email': user.email, 'callback_url': cburl,
                'order_number': order_no, 'currency': 'NGN'}

        # Make a call to paystack
        try:
            r = requests.post(curl, headers=headers, json=data)
            r.raise_for_status()  # Raise exception for HTTP errors
        except requests.exceptions.RequestException as e:
            messages.error(request, f'Error making payment: {e}')
        else:
            transback = json.loads(r.text)
            rdurl = transback['data']['authorization_url']

            account = Payment()
            account.user = user
            account.first_name = user.first_name
            account.last_name = user.last_name
            account.amount = total / 100
            account.paid = True
            account.additional_info = add_info
            account.pay_code = ref
            account.save()

            return redirect(rdurl)

    return redirect('checkout')


@login_required(login_url='signin')
def callback(request):
    userprof = Customer.objects.get(user__username=request.user.username)
    cart = Cart.objects.filter(user__username=request.user.username, paid=False)
    cars = []

    for item in cart:
        item.paid = True
        item.save()
        
        items = Product.objects.get(pk=item.items.id)
        

    context = {
        'userprof': userprof,
        'cart': cart,
        'items': items,
    }

    return render(request, 'callback.html', context)


def search(request):
    if request.method == 'POST':
        items = request.POST['search']
        searched = Q(model__icontains=items)| Q(description__icontains=items)| Q(price__icontains=items)| Q(promo_price__icontains=items)| Q(condition__icontains=items)
        searched_item = Product.objects.filter(searched)
        
        context = {
            'items':items,
            'searched_item':searched_item
        }
        
        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')
    
    
def subscribes(request):
    products = Subscribe.objects.all()
    p = Paginator(products, 12)
    page = request.GET.get('page')
    pagin = p.get_page(page)
    
    context = {
        'pagin': pagin,
    }
    
    return render(request, 'subscribes.html', context)




    
    

