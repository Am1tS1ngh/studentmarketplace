from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect , HttpResponse
from .models import Profile
from products.models import *
from accounts.models import Cart, CartItems
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)


        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request , 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout Successfully')
    return  render(request , 'accounts/login.html')
def register_page(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        college_id = request.POST.get('college_id')
        college_name = request.POST.get('college_name')
        contact_number = request.POST.get('contact_number')
        street_address = request.POST.get('street_address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        user_obj = User.objects.filter(username = email)
        if user_obj.exists():
            messages.warning(request, 'Email is already registered.')
            return HttpResponseRedirect(request.path_info)
        user_obj = User.objects.create(first_name = first_name , last_name = last_name, email = email, username = email)
        user_obj.set_password(password)
        user_obj.save()
        user_data = {'user': User.objects.get(username = email)}
        profile  = Profile.objects.get(user = user_data['user'].id)
        profile.college_id = college_id
        profile.college_name = college_name
        profile.contact_number = contact_number
        profile.street_address = street_address
        profile.state = state
        profile.city = city
        profile.pincode = pincode 
        profile.save()

        messages.success(request, 'An email has been sent on your email.')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/register.html')




def activate_email(request, email_token):
    try: 
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')



def add_to_cart(request , uid):
    if request.user.is_authenticated:
        variant = request.GET.get('variant')
        product = Product.objects.get(uid = uid)
        user = request.user
        cart , _ = Cart.objects.get_or_create(user = user , is_paid= False)
        cart_item = CartItems.objects.create(cart = cart , product = product)

        if variant:
            variant = request.GET.get('variant')
            size_variant = SizeVariant.objects.get(size_name = variant)
            cart_item.size_variant = size_variant
            cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, 'To add to cart, you should sign in')
        return render(request , 'accounts/login.html')



def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid = cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def cart(request):
    if request.user.is_authenticated:
        cart_obj = Cart.objects.get(is_paid = False, user = request.user)
        if request.method == 'POST':
            coupon = request.POST.get('coupon')
            coupon_obj = Coupon.objects.filter(coupon_code = coupon)
            if not coupon_obj.exists():
                messages.warning(request,"Invalid Coupon code.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if cart_obj.coupon:
                messages.warning(request,"Coupon already applied.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
            if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
                messages.warning(request, f"Amount should be greater than {coupon_obj[0].minimum_amount}.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
            if coupon_obj[0].is_expired:
                messages.wrong(request, "Coupon expired.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            cart_obj.coupon = coupon_obj[0]
            cart_obj.save()
            messages.success(request, "Coupon applied.")
        context = {'cart' : cart_obj}
        return render(request , 'accounts/cart.html', context )
    messages.warning(request, "🤦‍♂️To Get Carts🛒 you should 🙋sign in!")
    return render(request , 'accounts/login.html')



def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid = cart_id)
    cart.coupon = None
    cart.save()
    messages.debug(request, "Coupon removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def contact_seller(request, uid):
    if request.user.is_authenticated:
        product = Product.objects.get(uid = uid)
        user_data = {'user': User.objects.get(username = request.user.username)}
        profile  = Profile.objects.get(user = user_data['user'].id)
        subject = f"{request.user.first_name} requested to Buy."
        email_from = settings.EMAIL_HOST_USER
        message = f'{request.user.first_name} {request.user.last_name} wants to Buy {product.product_name}. \nContact Details {request.user.username} \nMobile Number {profile.contact_number} \n'
        email = product.product_seller.user.username
        print(email)
        send_mail(subject , message , email_from , [email])
        messages.success(request, f'{product.product_seller.user.first_name} {product.product_seller.user.last_name} will contact you soon!😊')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    messages.warning(request,"🤦‍♂️ To Contact Seller Sign In! ")
    return render(request , 'accounts/login.html')