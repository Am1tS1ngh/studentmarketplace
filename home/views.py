from django.shortcuts import render
from products.models import Product
from accounts.models import *
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_data = {'user': User.objects.get(username = request.user.username)}
        profile  = Profile.objects.get(user = user_data['user'].id)
        user_college = profile.college_name
        context = {'products' : Product.objects.filter(seller_college = user_college), 'all_products' : Product.objects.all()}
        return render(request , 'home/index.html', context)
    context = {'all_products' : Product.objects.all()}
    return render(request , 'home/index.html', context)
    

def faltu(request):
    return render(request , 'home/faltu.html')