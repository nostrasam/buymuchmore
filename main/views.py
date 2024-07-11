import uuid
import json
import requests


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.core.mail import EmailMessage 
from django.db.models import Q
from main.models import *
from .forms import *
from .models import Customer, Product, FeatureProduct, Review, Cart, Merchant
from django.db.models import Sum
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from geopy.distance import geodesic
from django.http import JsonResponse
from .utils import find_nearest_location



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
    p = Paginator(products, 16)
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
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email verification
            user.save()

            address = request.POST.get('address')
            phone = request.POST.get('phone')
            pix = request.POST.get('pix')

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

            # Generate email verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Generate email verification link
            verification_link = request.build_absolute_uri(
                reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
            )

            # Send verification email
            subject = 'Verify your email address'
            message = f"""
            Hi {user.first_name},

            Thank you for registering on our platform. Please click the link below to verify your email address:

            {verification_link}

            If you did not make this request, you can ignore this email.

            Thank you!
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, f'Dear {user.username}, your account is successfully created. Please check your email to verify your account.')
            return redirect('signin')
        else:
            # Pass form errors to the template for display
            messages.error(request, form.errors)

    return render(request, 'register.html', {'form': form})


def merchregistration(request):
    form = MerchantForm()

    if request.method == 'POST':
        form = MerchantForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email verification
            user.save()

            address = request.POST['address']
            address_type = request.POST['address_type']
            phone = request.POST['phone']
            pix = request.POST['pix']
            company_name = request.POST['company_name']
            company_registration = request.POST['company_registration']
            business_sector = request.POST['business_sector']

            # Create and save Merchant object
            new_merchant = Merchant(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=phone,
                company_name=company_name,
                company_registration=company_registration,
                business_sector=business_sector,
                address=address,
                address_type=address_type,
                pix=pix
            )
            new_merchant.save()

            # Generate email verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Generate email verification link
            verification_link = request.build_absolute_uri(
                reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
            )

            # Send verification email
            subject = 'Verify your email address'
            message = f"""
            Hi {user.first_name},

            Thank you for registering on our platform. Please click the link below to verify your email address:

            {verification_link}

            If you did not make this request, you can ignore this email.

            Thank you!
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, f'Dear {user.username}, your account is successfully created. Please check your email to verify your account.')
            return redirect('merchsignin')
        else:
            messages.error(request, form.errors)

    return render(request, 'merchregistration.html', {'form': form})

def partnerregistration(request):
    form = MerchantForm()

    if request.method == 'POST':
        form = MerchantForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email verification
            user.save()

            address = request.POST['address']
            address_type = request.POST['address_type']
            phone = request.POST['phone']
            pix = request.POST['pix']
            company_name = request.POST['company_name']
            company_registration = request.POST['company_registration']
            business_sector = request.POST['business_sector']

            # Create and save Merchant object
            new_merchant = Merchant(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=phone,
                company_name=company_name,
                company_registration=company_registration,
                business_sector=business_sector,
                address=address,
                address_type=address_type,
                pix=pix
            )
            new_merchant.save()

            # Generate email verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Generate email verification link
            verification_link = request.build_absolute_uri(
                reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
            )

            # Send verification email
            subject = 'Verify your email address'
            message = f"""
            Hi {user.first_name},

            Thank you for registering on our platform. Please click the link below to verify your email address:

            {verification_link}

            If you did not make this request, you can ignore this email.

            Thank you!
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, f'Dear {user.username}, your account is successfully created. Please check your email to verify your account.')
            return redirect('merchsignin')
        else:
            messages.error(request, form.errors)

    return render(request, 'partnerregistration.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified successfully.')
        return redirect('merchsignin')
    else:
        messages.error(request, 'The verification link is invalid.')
        return redirect('merchregistration')
     
         
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


def kyc_upload(request):
    userprof = Merchant.objects.get(user__username = request.user.username)
    pform = MerchantProfileForm(instance=request.user.merchant)
    if request.method == 'POST':
        pform = MerchantProfileForm(request.POST, request.FILES, instance=request.user.merchant)
        if pform.is_valid():
            user = pform.save()
            new = user.first_name.title()
            messages.success(request, f"dear {new} your document has been uploaded successfully. Please make your subscription payment and wait for 24 to 48 hours for account validation as a merchant!")
            return redirect('kyc_upload')
        else:
            new = user.first_name.title()
            messages.error(request, f'dear {new} your document upload generated the follow error: {pform.errors}')
            return redirect('kyc_upload')
        
    context = {
        'userprof':userprof
    }
    
    return render(request, 'kyc_upload.html', context)


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
        cburl = 'http://34.224.69.100/callback'  # Payment thank you page
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


@login_required
def find_nearest_seller(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer_location = (customer.latitude, customer.longitude)

    merchants = Merchant.objects.filter(address_type=Merchant.SELLER_ADDRESS)
    seller_locations = [
        {
            'latitude': merchant.latitude,
            'longitude': merchant.longitude,
            'address': merchant.address,
            'address_type': 'Seller',
            'company_name': merchant.company_name,  # Assuming company_name field exists
            'phone': merchant.phone  # Assuming phone field exists
        } 
        for merchant in merchants
    ]

    nearest_seller, distance = find_nearest_location(customer_location, seller_locations)

    context = {
        'address': nearest_seller['address'],
        'address_type': nearest_seller['address_type'],
        'distance': distance,
        'company_name': nearest_seller['company_name'],
        'phone': nearest_seller['phone']
    }

    return render(request, 'nearest_seller.html', context)


@login_required
def find_nearest_delivery_service(request, merchant_id):
    merchant = get_object_or_404(Merchant, pk=merchant_id)
    merchant_location = (merchant.latitude, merchant.longitude)

    # Filter out the merchant itself and include only DELIVERY_SERVICE_ADDRESS type
    delivery_locations = Merchant.objects.filter(address_type=Merchant.DELIVERY_SERVICE_ADDRESS).exclude(id=merchant_id)

    delivery_locations_list = [
        {
            'id': location.id,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'address': location.address,
            'address_type': location.address_type,
            'company_name': location.company_name,
            'phone': location.phone
        }
        for location in delivery_locations
    ]

    nearest_delivery_service, shortest_distance = find_nearest_location(merchant_location, delivery_locations_list)

    if nearest_delivery_service:
        context = {
            'merchant': merchant,
            'nearest_service': nearest_delivery_service,
            'distance': shortest_distance
        }
    else:
        context = {
            'merchant': merchant,
            'error': 'No delivery services found nearby.'
        }

    return render(request, 'nearest_delivery_service.html', context)



def merchant_dashboard(request):
    search_query = request.GET.get('search', '')
    merchants = Merchant.objects.filter(company_name__icontains=search_query, email__icontains=search_query, address__icontains=search_query)  # Adjusted the filter field to company_name
    context = {
        'merchants': merchants,
        'search_query': search_query,
    }
    return render(request, 'merchant_dashboard.html', context)



    