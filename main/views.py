import uuid
import json
import requests
import stripe
import time 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from .forms import ProductForm
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.db.models import Q
from django.db import IntegrityError
from main.models import *
from .forms import *
from .models import Customer, Product, FeatureProduct, Review, Cart, Merchant, ProductRating, Payment
from .models import Order
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Case, When, IntegerField, F, Sum, Value
from django.db.models import Sum   
from sklearn.cluster import KMeans
import numpy as np
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from geopy.distance import geodesic
from django.http import JsonResponse
from .utils import find_nearest_location
import random
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, F
from decimal import Decimal, ROUND_HALF_UP
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, get_current_timezone
from django.utils.http import urlencode
from django.core.signing import Signer, BadSignature, SignatureExpired, TimestampSigner





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
    # Get the specific product or return 404 if not found
    merchant_det = get_object_or_404(Product, pk=id, slug=slug)
    
    # Get similar products by type and randomly select 5
    similar_products = Product.objects.filter(type=merchant_det.type).exclude(id=id).order_by('?')[:5]  # Randomly limiting to 5 similar products

    # Context data for rendering the template
    context = {
        'merchant_det': merchant_det,
        'similar_products': similar_products,
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

            # Send email after form submission
            send_mail(
                subject='New Contact Form Submission',  # Email subject
                message=f"You have a new message from {form.cleaned_data['name']}:\n\n{form.cleaned_data['message']}",  # The message content
                from_email=form.cleaned_data['email'],  # Sender's email
                recipient_list=['buymuchmoree@gmail.com'],  # Recipient's email
                fail_silently=False,  # Raise error if email fails to send
            )

            messages.success(request, "Your message has been sent successfully!!!")
            return redirect('home')

    context = {
        'form': form,
    }

    return render(request, 'contact.html', context)


def signout(request):
    logout(request)
    messages.success(request, 'you are now signed out')
    return redirect('signin')


# Helper function to transfer session cart to user's cart after login/registration
def transfer_session_cart_to_user(request, user):
    session_cart = request.session.get('cart', {})
    
    if session_cart:
        for item_id, item_data in session_cart.items():
            main = get_object_or_404(Product, pk=item_id)
            # Check if the item is already in the user's cart
            cart_item = Cart.objects.filter(user=user, items=main, paid=False).first()
            
            if cart_item:
                # Update the quantity and amount if item already exists in the cart
                cart_item.quantity += item_data['quantity']
                cart_item.amount = cart_item.quantity * cart_item.price
                cart_item.save()
            else:
                # Create a new cart entry for the user
                Cart.objects.create(
                    user=user,
                    items=main,
                    quantity=item_data['quantity'],
                    price=item_data['price'],
                    amount=item_data['amount'],
                    paid=False
                )
        
        # Clear the session cart after transferring to the user's cart
        del request.session['cart']
        request.session.modified = True  # Mark session as modified to ensure changes are saved

# Signin view
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Login successful!')

            # Transfer session cart items to user after login
            transfer_session_cart_to_user(request, user)

            return redirect('home')  # Redirect to home or wherever you want
        else:
            messages.error(request, 'Username/password is incorrect. Please try again.')
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
            return redirect('staff_product_list')
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
            Hi {user.username},

            Thank you for registering on our platform. Please click the link below to verify your email address:

            {verification_link}

            If you did not make this request, you can ignore this email.

            Thank you!
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, f'Dear {user.username}, your account is successfully created. Please check your email to verify your account.')
            return redirect('reg_success')
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
            Hi {user.username},

            Thank you for registering on our platform. Please click the link below to verify your email address:

            {verification_link}

            If you did not make this request, you can ignore this email.

            Thank you!
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, f'Dear {user.username}, your account is successfully created. Please check your email to verify your account.')
            return redirect('reg_success')
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
            Hi {user.username},

            Thank you for registering on our platform. Please click the link below to verify your email address:

            {verification_link}

            If you did not make this request, you can ignore this email.

            Thank you!
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, f'Dear {user.username}, your account is successfully created. Please check your email to verify your account.')
            return redirect('reg_success')
        else:
            messages.error(request, form.errors)

    return render(request, 'partnerregistration.html', {'form': form})



User = get_user_model()

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if User.objects.filter(email=user.email, is_active=True).exists():
            messages.error(request, 'This email is already associated with another account.')
            return redirect('signin')  # Ensure the name 'registration' matches the one in urls.py

        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified successfully.')
        return redirect('signin')
    else:
        messages.error(request, 'The verification link is invalid.')
        return redirect('registration')  # Ensure this name exists


@login_required(login_url='signin')
def profile(request):
    try:
        # Fetch the customer profile for the logged-in user
        userprof = Customer.objects.get(user__username=request.user.username)
        # Fetch the paid cart items for the logged-in user
        cart = Cart.objects.filter(user=request.user, status='paid')

        context = {
            'userprof': userprof,
            'cart': cart,
        }

        return render(request, 'profile.html', context)

    except Customer.DoesNotExist:
        # If the customer does not exist, redirect to the KYC page
        return redirect('kyc_upload')  # Make sure 'kyc' is the correct URL pattern for the KYC page


@login_required(login_url='signin')
def merchprofile(request):
    userprof = Merchant.objects.get(user__username=request.user.username)

    context = {
        'userprof': userprof
    }

    return render(request, 'merchprofile.html', context)

@login_required(login_url='signin')
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


@login_required
def kyc_upload(request):
    # Fetch the Merchant profile for the logged-in user
    userprof = Merchant.objects.get(user__username=request.user.username)
    pform = MerchantProfileForm(instance=request.user.merchant)

    if request.method == 'POST':
        # Handle form data and file uploads
        pform = MerchantProfileForm(request.POST, request.FILES, instance=request.user.merchant)
        
        if pform.is_valid():
            user = pform.save()  # Save the user's updated profile
            new = user.first_name.title()

            # Send success message
            messages.success(request, f"Dear {new}, your document has been uploaded successfully. "
                                      "Please wait for 24 to 48 hours for account activation as a merchant!")

            # If the user uploaded a file
            if 'pix' in request.FILES:
                uploaded_file = request.FILES['pix']
                
                # Prepare the email to send the uploaded file
                email = EmailMessage(
                    subject="New KYC Document Uploaded",
                    body=f"Dear Admin,\n\nA new KYC document has been uploaded by {new}.\n\nPlease find the document attached.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=['buymuchmoree@gmail.com', 'nostrasam@yahoo.com'],  # Multiple recipients
                )
                
                # Attach the uploaded file
                email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
                
                # Send the email
                email.send()

            # Redirect back to the KYC upload page after a successful upload
            return redirect('kyc_upload')
        else:
            new = user.first_name.title()
            # If the form is invalid, display an error message
            messages.error(request, f"Dear {new}, your document upload generated the following error: {pform.errors}")
            return redirect('kyc_upload')

    # Render the KYC upload form with the user's profile data
    context = {
        'userprof': userprof
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


def add_to_cart(request):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        itemsid = request.POST['itemsid']

        # Fetch the product or return 404 if not found
        main = get_object_or_404(Product, pk=itemsid)

        # Check the total quantity already purchased for this product
        paid_count = Cart.objects.filter(items=main, paid=True).aggregate(Sum('quantity'))['quantity__sum'] or 0

        # Check if the product availability is "No" or if paid_count has reached total stock
        if main.availability.lower() == 'no' or paid_count >= main.quantity:
            messages.error(request, 'This product is no longer available as it is sold out.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # Ensure requested quantity does not exceed available stock
        if quantity > main.quantity - paid_count:
            messages.error(request, 'Requested quantity exceeds available stock.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # Calculate the amount as a float, keeping the precision of price
        amount = float(main.price) * quantity

        # For non-logged-in users (new customers)
        if not request.user.is_authenticated:
            # Handle the cart in the session for new customers (not logged in)
            cart = request.session.get('cart', {})

            if itemsid in cart:
                if cart[itemsid]['quantity'] + quantity > main.quantity - paid_count:
                    messages.error(request, 'Cannot update cart due to shortage of items.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                
                cart[itemsid]['quantity'] += quantity
                cart[itemsid]['amount'] = float(main.price) * cart[itemsid]['quantity']
            else:
                cart[itemsid] = {
                    'itemsid': itemsid,
                    'quantity': quantity,
                    'price': float(main.price),
                    'amount': amount
                }
            
            request.session['cart'] = cart
            messages.success(request, 'Item added to cart. Please register or log in to complete the purchase.')
            return redirect('signin')

        # For logged-in users
        else:
            cart = Cart.objects.filter(user=request.user, paid=False)

            # Check if the item is already in the user's cart
            basket = cart.filter(items=main).first()
            if basket:
                if basket.quantity + quantity > main.quantity - paid_count:
                    messages.error(request, 'Cannot update cart due to shortage of items.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                
                basket.quantity += quantity
                basket.amount = basket.quantity * float(main.price)
                basket.save()
                messages.success(request, 'One item added to cart.')
            else:
                if quantity > main.quantity - paid_count:
                    messages.error(request, 'Requested quantity exceeds available stock.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                
                Cart.objects.create(
                    user=request.user,
                    items=main,
                    quantity=quantity,
                    price=float(main.price),
                    amount=float(amount),
                    paid=False
                )
                messages.success(request, 'One item added to cart.')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def calculate_cart_totals(cart_items, service_type):
    subtotal = Decimal('0.00')
    total_vat = Decimal('0.00')
    is_vat_exempt = all(item.items.is_vat_exempt for item in cart_items)
    
    # Calculate subtotal and VAT
    for item in cart_items:
        item_subtotal = item.price * item.quantity
        subtotal += item_subtotal
        
        if not item.items.is_vat_exempt:
            vat_rate = Decimal('0.20')
            item_vat = (vat_rate * item_subtotal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total_vat += item_vat
    
    # Internal base commission (hidden from customer)
    base_commission = (Decimal('0.08') * subtotal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Set additional commission rate based on service type
    additional_commission_rate = Decimal('0.08') if service_type == 'regular' else Decimal('0.12')
    additional_commission = (additional_commission_rate * subtotal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Total for customer, including VAT if applicable
    total_for_customer = (subtotal + additional_commission + (0 if is_vat_exempt else total_vat)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return {
        'subtotal': subtotal,
        'base_commission': base_commission,
        'additional_commission': additional_commission,
        'vat': total_vat if not is_vat_exempt else 0,
        'total': total_for_customer,
        'is_vat_exempt': is_vat_exempt,
    }


@login_required(login_url='signin')
def cart(request):
    if request.user.is_authenticated:
        # Fetch all unpaid cart items for the logged-in user
        cart_items = Cart.objects.filter(user=request.user, paid=False)
        
        # Get the selected service type or default to 'regular'
        service_type = request.POST.get('service_type', 'regular')
        
        # Calculate cart totals
        totals = calculate_cart_totals(cart_items, service_type)
        
        # Identify canceled orders
        canceled_orders = Cart.objects.filter(user=request.user, paid=False, status='canceled')
        
        context = {
            'cart': cart_items,
            'subtotal': totals['subtotal'],
            'base_commission': totals['base_commission'],
            'additional_commission': totals['additional_commission'],
            'vat': totals['vat'],
            'total': totals['total'],
            'total_quantity': cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0,
            'service_type': service_type,
            'is_vat_exempt': totals['is_vat_exempt'],
            'canceled_orders': canceled_orders,  # Include canceled orders in the context
        }
        
        return render(request, 'cart.html', context)
    
    # Redirect to login page if the user is not authenticated
    return render(request, 'login.html', {'error': 'You need to be logged in to view your cart.'})



@login_required(login_url='signin')
def delete(request):
    if request.method == 'POST':
        del_item = request.POST['delid']
        Cart.objects.filter(pk=del_item).delete()
        messages.success(request, 'One item deleted')
        return redirect('cart')
    

@login_required(login_url='signin')   
def update(request):
    if request.method == 'POST':
        qty_item = request.POST.get('quantid')
        new_qty = int(request.POST.get('quant'))

        # Fetch the cart item based on the provided ID
        newqty = Cart.objects.get(pk=qty_item)

        # Get the unpaid count for the product
        unpaid_count = newqty.items.quantity - Cart.objects.filter(items=newqty.items, paid=True).count()

        if new_qty > unpaid_count:
            # If the requested quantity exceeds the available unpaid stock, show an error
            messages.error(request, f'Sorry, only {unpaid_count} items are left in stock.')
            return redirect('cart')

        # Convert price and quantity to Decimal to prevent TypeError
        price = Decimal(newqty.price)
        quantity = Decimal(new_qty)

        # Update the quantity and amount in the cart if the request is valid
        newqty.quantity = quantity
        newqty.amount = price * quantity

        # Save the updated cart item
        newqty.save()

        messages.success(request, 'Quantity updated.')
        return redirect('cart')



stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='signin')
def checkout(request):
    if request.method == 'POST':
        service_type = request.POST.get('service_type', 'regular')
        cart_items = Cart.objects.filter(user=request.user, paid=False)
        totals = calculate_cart_totals(cart_items, service_type)
        order_number = str(uuid.uuid4())

        try:
            # Retrieve or create Stripe customer
            user_profile = Customer.objects.get(user=request.user)
            if not user_profile.stripe_customer_id:
                customer = stripe.Customer.create(
                    email=request.user.email,
                    name=f'{request.user.first_name} {request.user.last_name}',
                )
                user_profile.stripe_customer_id = customer.id
                user_profile.save()
            else:
                customer = stripe.Customer.retrieve(user_profile.stripe_customer_id)

            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {'name': 'Your Cart Total'},
                        'unit_amount': int(totals['total'] * 100),  # Stripe expects amount in pence
                    },
                    'quantity': 1,
                }],
                mode='payment',
                customer=customer.id,
                success_url=f'http://shopmuchmore.co.uk/payment/success/?session_id={{CHECKOUT_SESSION_ID}}&order_number={order_number}',
                cancel_url='http://shopmuchmore.co.uk/payment/cancelled/',
                metadata={
                    'user_id': request.user.id,
                    'order_number': order_number,
                    'service_type': service_type,
                    'vat_exempt': totals['is_vat_exempt']
                }
            )
            return redirect(checkout_session.url, code=303)
        
        except Exception as e:
            return render(request, 'checkout_error.html', {'error': str(e)})

    return redirect('cart')


def pay(request):
    if request.method == 'POST':
        try:
            # Generate a unique order number
            order_number = str(uuid.uuid4()).split('-')[0]

            # Get total amount in GBP from the form (in pence)
            total_amount = float(request.POST.get('total', 0)) * 100  # Convert to pence

            # Create Stripe Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': 'Your Product Name',
                        },
                        'unit_amount': int(total_amount),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/payment-success/') + f'?session_id={{CHECKOUT_SESSION_ID}}&order_number={order_number}',
                cancel_url=request.build_absolute_uri('/payment-cancelled/'),
                metadata={
                    'order_number': order_number,
                    'user_id': request.user.id,
                }
            )

            # Redirect the user to Stripe's checkout page
            return redirect(session.url)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)

    return render(request, 'checkout.html')



def payment_success(request):
    session_id = request.GET.get('session_id')
    order_number = request.GET.get('order_number')
    if not session_id:
        return render(request, 'payment_error.html', {'message': 'No session ID provided'})

    try:
        # Retrieve Stripe session and customer data
        session = stripe.checkout.Session.retrieve(session_id)
        customer_data = stripe.Customer.retrieve(session.customer)
        customers = Customer.objects.filter(email=customer_data.email)
        userprof = customers.first() if customers.exists() else Customer.objects.create(email=customer_data.email, user=request.user)

        # Get cart items
        cart = Cart.objects.filter(user__email=customer_data.email, paid=False)
        if not cart.exists():
            return render(request, 'payment_error.html', {'message': 'No items in the cart'})

        service_type = session.metadata.get('service_type', 'regular')
        totals = calculate_cart_totals(cart, service_type)
        stripe_total_amount = Decimal(session.amount_total) / Decimal(100)
        cart_items = []
        items_list = []

        # Process cart items
        for item in cart:
            item.paid = True
            item.order_number = order_number
            item.save()

            product = Product.objects.get(pk=item.items.id)
            items_list.append(f"<tr><td>{product.model}</td><td>{item.quantity}</td><td>£{item.price}</td></tr>")
            cart_items.append({'product': product, 'quantity': item.quantity, 'price': item.price})

        # Record the payment
        Payment.objects.create(
            user=request.user,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            amount=session.amount_total,
            paid=True,
            phone=userprof.phone,
            pay_code=order_number,
            additional_info=f"Order Number: {order_number}, Total: £{stripe_total_amount:.2f}"
        )

        # Prepare email content for the customer
        email_subject = f'Your Order Confirmation - {order_number}'
        html_content = f"""
        <html>
        <body>
        <p>Dear {userprof.user.username},</p>
        <p>Thank you for your purchase! Your order number is: <strong>{order_number}</strong>.</p>
        <p>Your order includes the following items:</p>
        <table border="1" cellpadding="10" cellspacing="0">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Quantity</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                {''.join(items_list)}
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="2">Delivery Fee</td>
                    <td><strong>£{totals['additional_commission']:.2f}</strong></td>
                </tr>
                <tr>
                    <td colspan="2"><strong>VAT</strong></td>
                    <td><strong>£{totals['vat']:.2f}</strong></td>
                </tr>
                <tr>
                    <td colspan="2"><strong>Total</strong></td>
                    <td><strong>£{stripe_total_amount:.2f}</strong></td>
                </tr>
            </tfoot>
        </table>
        <p>We will notify you once your items are shipped.</p>
        <p>Please contact us within 30 minutes of payment confirmation to cancel your order at contactus@buymuchmore.co.uk</p>
        <p>Thank you for shopping with us!</p>
        <p>Best regards,<br>Buy Much More Team</p>
        </body>
        </html>
        """
        plain_message = strip_tags(html_content)

        # Send email to the customer
        send_email_notification(email_subject, plain_message, html_content, [customer_data.email])

        # Notify each seller or merchant
        for item in cart:
            product = item.items
            # Fetch seller email from the Merchant Registration table
            seller_email = product.seller.merchant_registration.email  # Ensure the relationship exists and is correct
            if seller_email:
                seller_subject = f'Order Alert - {order_number}'
                seller_message = f"""
                Dear {product.seller.name},
                You have received a new order for your product "{product.model}".
                Order Number: {order_number}
                Quantity: {item.quantity}
                Price: £{item.price}
                """
                send_email_notification(seller_subject, seller_message, seller_message, [seller_email])

        # Send a copy to admin
        send_email_notification(email_subject, plain_message, html_content, ['buymuchmoree@gmail.com'])

        # Clear the cart after payment
        cart.delete()

        # Set up cancellation context
        current_time = datetime.now()
        order_time = session.created  # Assuming 'created' is a Unix timestamp
        cancellation_deadline = datetime.fromtimestamp(order_time) + timedelta(minutes=30)
        can_cancel = current_time <= cancellation_deadline

        # Render success page
        context = {
            'userprof': userprof,
            'customer_email': customer_data.email,
            'order_number': order_number,
            'subtotal': totals['subtotal'],
            'commission': totals['additional_commission'],
            'vat': totals['vat'],
            'total_price': stripe_total_amount,
            'cart_items': cart_items,
            'service_type': service_type,
            'is_vat_exempt': totals.get('is_vat_exempt', False),
            'can_cancel': can_cancel,
            'cancel_deadline': cancellation_deadline.strftime('%Y-%m-%d %H:%M:%S')
        }

        return render(request, 'payment_success.html', context)

    except stripe.error.StripeError as e:
        return render(request, 'payment_error.html', {'message': str(e)})



def send_email_notification(subject, plain_message, html_message, recipient_list):
    email = EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    email.attach_alternative(html_message, "text/html")
    email.send()


def payment_cancelled(request):
    # Stripe checkout cancelled page
    messages.error(request, "Payment was cancelled.")
    return render(request, 'payment_cancelled.html')


stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_email = session['customer_details']['email']
        order_number = session['metadata'].get('order_number')

        userprof = Customer.objects.get(user__email=user_email)
        cart = Cart.objects.filter(user__email=user_email, paid=False)

        if not cart.exists():
            return HttpResponse("No items in the cart", status=404)

        # Commission and total calculations
        service_type = session['metadata'].get('service_type', 'regular')
        commission_rate = 0.22 if service_type == 'premium' else 0.15
        subtotal = sum(item.price * item.quantity for item in cart)
        commission = commission_rate * subtotal
        vat = 0.20 * subtotal
        total_price = subtotal + commission + vat

        # Mark cart items as paid and save order information
        for item in cart:
            item.paid = True
            item.order_number = order_number
            item.service_type = service_type
            item.save()

        # Clear the cart after payment
        cart.delete()

        # Prepare email content
        items_list = [
            f"<tr><td>{Product.objects.get(pk=item.items.id).model}</td><td>{item.quantity}</td><td>£{item.price:.2f}</td></tr>"
            for item in cart
        ]

        email_subject = f'Your Order Confirmation - {order_number}'
        html_content = f"""
        <html>
        <body>
        <p>Dear {userprof.user.username},</p>
        <p>Your order number is: <strong>{order_number}</strong>.</p>
        <table border="1">
            <tr><th>Product</th><th>Quantity</th><th>Price</th></tr>
            {''.join(items_list)}
        </table>
        <p>Subtotal: £{subtotal:.2f}</p>
        <p>Commission: £{commission:.2f}</p>
        <p>VAT: £{vat:.2f}</p>
        <p><strong>Total: £{total_price:.2f}</strong></p>
        <p>Thank you for shopping with us!</p>
        </body>
        </html>
        """

        # Send email to the customer
        send_email(email_subject, html_content, user_email)
        # Send email to the admin/seller
        send_email(email_subject, html_content, 'buymuchmoree@gmail.com')

        return HttpResponse(status=200)

    return HttpResponse(status=400)


def send_email(subject, content, recipient):
    email = EmailMultiAlternatives(subject, strip_tags(content), settings.DEFAULT_FROM_EMAIL, [recipient])
    email.attach_alternative(content, "text/html")
    email.send(fail_silently=False)


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


# Function to apply K-means clustering based on price and availability
def cluster_product(products, num_clusters=4):
    # Filter products to only include those that are available
    available_products = [p for p in products if p.availability.lower() == 'yes']
    
    # Use price only for clustering since availability is already filtered
    product_features = np.array([[p.price] for p in available_products])

    # Apply K-means clustering if there are enough products, otherwise skip clustering
    if len(available_products) >= num_clusters:
        kmeans = KMeans(n_clusters=num_clusters, random_state=1)
        kmeans.fit(product_features)
        
        # Group products by cluster
        clustered_product = {i: [] for i in range(num_clusters)}
        for i, product in enumerate(available_products):
            cluster = kmeans.labels_[i]
            clustered_product[cluster].append(product)
    else:
        # If fewer products than clusters, treat each product as its own "cluster"
        clustered_product = {i: [p] for i, p in enumerate(available_products)}

    return clustered_product

# Fetching similar products based on cluster and lowest price
def get_similar_product(target_product, products, num_clusters=4):
    clustered_product = cluster_product(products, num_clusters)
    
    # Identify target product's cluster
    target_cluster = None
    for cluster, items in clustered_product.items():
        if target_product in items:
            target_cluster = cluster
            break

    if target_cluster is not None:
        # Get similar products from the same cluster, excluding the target product itself
        similar_products = [p for p in clustered_product[target_cluster] if p != target_product]
        
        # Sort similar products by price (ascending order) to prioritize the lowest priced products
        similar_products.sort(key=lambda x: x.price)
        
        # Limit the display to a maximum of 4 items
        return similar_products[:4]
    else:
        return []
 


def cluster_product_by_category(products, target_category, num_clusters=4):
    """
    Clusters products by price for a specific category.
    """
    # Filter products by target category and availability
    category_products = [p for p in products if p.type == target_category and p.availability.lower() == 'yes']
    
    # If no products are available in the category, return empty clusters
    if not category_products:
        return {i: [] for i in range(num_clusters)}

    # Use price as the feature for clustering
    product_features = np.array([[p.price] for p in category_products])

    # Apply K-means clustering if there are enough products; otherwise, treat each as its own cluster
    if len(category_products) >= num_clusters:
        kmeans = KMeans(n_clusters=num_clusters, random_state=1)
        kmeans.fit(product_features)
        
        # Group products by cluster
        clustered_product = {i: [] for i in range(num_clusters)}
        for i, product in enumerate(category_products):
            cluster = kmeans.labels_[i]
            clustered_product[cluster].append(product)
    else:
        # If fewer products than clusters, treat each product as its own "cluster"
        clustered_product = {i: [p] for i, p in enumerate(category_products)}

    return clustered_product


def get_similar_lower_price_products(target_product, products, num_display=4, sort_desc=False):
    """
    Fetches random products in the same category as the target product with the lowest prices.
    """
    # Filter products by the same category
    category_products = [p for p in products if p.type == target_product.type and p != target_product]

    # Sort products by price (ascending by default)
    category_products.sort(key=lambda x: x.price, reverse=sort_desc)
    
    # Select a subset of the products (randomly shuffled if desired)
    random.shuffle(category_products)

    # Return up to the specified number of products
    return category_products[:num_display]


@login_required
def submit_rating(request, product_id):
    try:
        # Fetch the product early to avoid UnboundLocalError
        product = get_object_or_404(Product, id=product_id)
        
        if request.method == 'POST':
            rating = request.POST.get('rating')
            
            if rating is not None:
                try:
                    # Convert rating to float
                    rating = float(rating)
                    
                    # Ensure rating is between 0 and 5
                    if rating < 0 or rating > 5:
                        messages.error(request, "Invalid rating value. Rating must be between 0 and 5.")
                        return redirect('detail', id=product.id, slug=product.slug)

                    # Limit rating to one decimal place
                    rating = round(rating, 1)

                    # Check if the user has already rated the product
                    existing_rating = ProductRating.objects.filter(user=request.user, product=product).first()
                    if existing_rating:
                        messages.error(request, "You have already rated this product.")
                        return redirect('detail', id=product.id, slug=product.slug)

                    # Ensure the product has an existing rating_value
                    if product.rating_value is None:
                        product.rating_value = 0
                        product.rating_count = 0

                    # Calculate the new average rating
                    total_rating = product.rating_value * product.rating_count
                    product.rating_count += 1
                    product.rating_value = round((total_rating + rating) / product.rating_count, 1)
                    product.save()

                    # Save the user's rating
                    ProductRating.objects.create(user=request.user, product=product, rating=rating)

                    messages.success(request, "Thank you for rating the product!")
                    return redirect('detail', id=product.id, slug=product.slug)
                except ValueError:
                    messages.error(request, "Invalid rating format. Please enter a valid number.")
                    return redirect('detail', id=product.id, slug=product.slug)
            else:
                messages.error(request, "Rating not provided.")
                return redirect('detail', id=product.id, slug=product.slug)
        else:
            return HttpResponse("Invalid request method", status=405)

    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('product_list')  # Redirect to a product listing page or home page
    
    
    from django.shortcuts import render

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_service(request):
    return render(request, 'terms_service.html')

def deletion_instruction(request):
    return render(request, 'deletion_instruction.html')

def user_manual(request):
    return render(request, 'user_manual.html')

def reg_success(request):
    return render(request, 'reg_success.html')


# View for staff to create products
@staff_member_required
@login_required(login_url='merchsignin')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller_name = request.user  # Associate the product with the logged-in staff user
            product.save()
            messages.success(request, 'Product successfully created!')
            return redirect('staff_product_list')  # Redirect to a page listing their products
    else:
        form = ProductForm()

    return render(request, 'create_product.html', {'form': form})



@staff_member_required
@login_required
def staff_product_list(request):
    products = Product.objects.filter(seller_name=request.user)
    total_products = products.count()

    product_data = []
    total_paid_value = 0
    total_unpaid_value = 0
    total_value_all_products = 0
    total_transaction_outstanding_balance = 0
    actual_payment = 0
    total_transaction_count = 0  # To track total transaction count

    current_time = timezone.now()

    for product in products:
        paid_orders = Cart.objects.filter(items=product, paid=True)
        unpaid_count = product.quantity - paid_orders.count()
        canceled_orders = Cart.objects.filter(items=product, paid=False, canceled=True)

        product_paid_value = paid_orders.count() * product.price
        product_unpaid_value = unpaid_count * product.price

        base_commission = (Decimal('0.08') * product_paid_value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        subtotal = product_paid_value - base_commission

        total_paid_value += subtotal
        total_unpaid_value += product_unpaid_value

        # Calculate total value for the product
        total_value_for_product = product.quantity * product.price
        total_value_all_products += total_value_for_product

        latest_transaction = product.price * product.quantity
        transaction_outstanding_balance = latest_transaction - subtotal
        total_transaction_outstanding_balance += transaction_outstanding_balance
        
        payment_deduction = total_paid_value + total_unpaid_value

        actual_payment = total_value_all_products - payment_deduction

        # Increment the transaction count
        total_transaction_count += paid_orders.count()

        most_recent_payment = Payment.objects.filter(
            pay_code__in=paid_orders.values_list('order_number', flat=True)
        ).order_by('-payment_date').first()

        most_recent_canceled_order = canceled_orders.order_by('-cancellation_time').first()

        # Determine order status and blinking logic
        order_status_color = 'orange'
        order_status_text = 'Pending'
        blink = False

        if most_recent_canceled_order:
            if most_recent_canceled_order.cancellation_time >= current_time - timezone.timedelta(minutes=5):
                order_status_color = 'red'
                order_status_text = 'Cancel'
                blink = True
            else:
                order_status_color = 'orange'
                order_status_text = 'Pending'
                blink = False
        elif most_recent_payment:
            if most_recent_payment.payment_date >= current_time - timezone.timedelta(minutes=5):
                order_status_color = 'green'
                order_status_text = 'Paid'
                blink = True
            else:
                order_status_color = 'orange'
                order_status_text = 'Pending'
                blink = False

        sales_data = []
        for paid_order in paid_orders:
            payment = Payment.objects.filter(pay_code=paid_order.order_number).first()
            payment_date = payment.payment_date if payment else None
            quantity_sold = paid_order.quantity
            amount_sold = quantity_sold * paid_order.price

            if payment:
                sales_data.append({
                    'order_time': payment_date,
                    'quantity_sold': quantity_sold,
                    'amount_sold': amount_sold,
                    'payment_amount': payment.amount,
                    'invoice_number': payment.invoice_number,
                    'pay_code': payment.pay_code,
                })

        min_aware_datetime = timezone.make_aware(timezone.datetime.min, timezone.get_current_timezone())
        sales_data = sorted(sales_data, key=lambda x: x['order_time'] or min_aware_datetime, reverse=True)

        most_recent_transaction = sales_data[0] if sales_data else None

        product_data.append({
            'id': product.id,
            'model': product.model,
            'quantity': product.quantity,
            'price': product.price,
            'uploaded_at': product.uploaded_at,
            'paid_count': paid_orders.count(),
            'unpaid_count': unpaid_count,
            'canceled_count': canceled_orders.count(),
            'total_value': total_value_for_product,
            'order_status_color': order_status_color,
            'order_status_text': order_status_text,
            'status': order_status_text,
            'blink': blink,
            'average_rating': product.get_average_rating(),
            'rating_count': product.rating_count,
            'most_recent_transaction': {
                'quantity': most_recent_transaction['quantity_sold'] if most_recent_transaction else None,
                'time': most_recent_transaction['order_time'] if most_recent_transaction else None,
                'payment_amount': most_recent_transaction['amount_sold'] if most_recent_transaction else None,
                'invoice_number': most_recent_transaction['invoice_number'] if most_recent_transaction else None,
                'pay_code': most_recent_transaction['pay_code'] if most_recent_transaction else None,
            } if most_recent_transaction else None,
        })

    context = {
        'products': product_data,
        'total_products': total_products,
        'total_paid_value': total_paid_value,
        'total_unpaid_value': total_unpaid_value,
        'total_value_all_products': total_value_all_products,
        'transaction_outstanding_balance': total_transaction_outstanding_balance,
        'actual_payment': actual_payment,  # Actual payment now matches the aggregate total
        'total_transaction_count': total_transaction_count,  # Total transaction count for the seller
    }

    return render(request, 'staff_product_list.html', context)


@staff_member_required
@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product successfully edited!')
            return redirect('staff_product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})



def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product successfully deleted!')
        return redirect('staff_product_list')  # Redirect after successful deletion
    return render(request, 'delete_product.html', {'product': product})



@login_required
def cancel_order(request):
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        cart_items = Cart.objects.filter(order_number=order_number, user=request.user, paid=True)

        # Check if the order exists and is valid for cancellation
        if not cart_items.exists():
            return render(request, 'error.html', {'message': 'Order not found or already canceled.'})

        first_item = cart_items.first()
        if now() - first_item.created_at > timedelta(minutes=30):
            return render(request, 'error.html', {'message': 'Cancellation period has expired.'})

        # Generate a secure cancellation link
        signer = TimestampSigner()
        try:
            cancel_token = signer.sign(order_number)
            cancel_url = f"{request.build_absolute_uri(reverse('cancel-confirm'))}?{urlencode({'token': cancel_token})}"
        except Exception as e:
            return render(request, 'error.html', {'message': f'Error generating cancellation link: {str(e)}'})

        # Send the cancellation link email
        recipient_list = ['buymuchmoree@gmail.com']
        if request.user.email:  # Include the user's email if available
            recipient_list.append(request.user.email)

        send_mail(
            subject=f"Order Cancellation Link: {order_number}",
            message=(
                f"Use the link below to confirm the cancellation of your order:\n"
                f"{cancel_url}\n\n"
                "Note: This link will expire in 30 minutes. Please note that refunds may take 12 to 24 hours to be processed and reflected in your account."
            ),
            from_email='noreply@buymuchmore.co.uk',
            recipient_list=recipient_list,
        )

        return render(request, 'success.html', {'message': 'Cancellation link has been sent to your email. You have 30 minutes to confirm your cancellation request.'})

    # Handle invalid request method
    return render(request, 'error.html', {'message': 'Invalid request.'})

@login_required
def confirm_cancel_order(request):
    token = request.GET.get('token')
    signer = TimestampSigner()

    try:
        # Verify and decode the token
        order_number = signer.unsign(token, max_age=1800)  # 30-minute expiration
        cart_items = Cart.objects.filter(order_number=order_number, user=request.user, paid=True)

        # Ensure the order exists and mark it as canceled
        if not cart_items.exists():
            return render(request, 'error.html', {'message': 'Invalid or already canceled order.'})

        for item in cart_items:
            item.paid = False
            item.canceled = True
            item.cancellation_time = now()
            item.save()

        return render(request, 'success.html', {'message': 'Your order has been successfully canceled.'})

    except SignatureExpired:
        return render(request, 'error.html', {'message': 'The cancellation link has expired.'})
    except BadSignature:
        return render(request, 'error.html', {'message': 'Invalid cancellation link.'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'An error occurred: {str(e)}'})
    

