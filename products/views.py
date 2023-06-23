from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from products.models import Product, SizeVariant, ColorVariant, Category, ProductImage
from django.template.defaultfilters import slugify
from django.contrib import messages
from accounts.models import *



# Create your views here.
def get_products(request, slug):
    try:
        product = Product.objects.get(slug = slug)
        context = {'product': product}
        product_quality = product.product_quality
        quality_list = []
        for i in range(product_quality):
            quality_list.append(i) 
        context['quality_list'] = quality_list
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size']  = size
            context['updated_price']  = price
        return render(request , 'product/product.html', context = context)

    except Exception as e: 
        print(e)
        return HttpResponseRedirect(request.path_info)




def insert_product(request):
    if request.user.is_authenticated:
        Size_Variant = SizeVariant.objects.all()
        Color_Variant = ColorVariant.objects.all()
        Categories = Category.objects.all()
        context = {"SizeVariant" : Size_Variant , "ColorVariant": Color_Variant, "Category": Categories}
        user_data = {'user': User.objects.get(username = request.user.username)}
        profile  = Profile.objects.get(user = user_data['user'].id)
        if request.method == "POST":
            product_seller = profile
            seller_college = profile.college_name
            product_name = request.POST.get("product_name")
            slug = slugify(product_name)
            category_uid = request.POST.get("category")
            price = request.POST.get("price")
            product_description = request.POST.get("description")
            product_quality = request.POST.get("product_quality")
            product_images = request.POST.getlist("images")
            print(product_images)
            color_Variant = request.POST.get("color_variant")
            size_Variant = request.POST.get("size_variant")
            product = Product(product_seller = product_seller, seller_college = seller_college, product_name = product_name, slug=slug ,category_id = category_uid,  price = price, product_description = product_description, product_quality=product_quality)

            if color_Variant is not None:
                product.color_Variant.set(color_Variant)
            if size_Variant is not None:
                product.size_Variant.set(size_Variant)
            product.save()
            for image in product_images:
                image_ = ProductImage(product_id = product.uid, image = image)
                image_.save()
            messages.success(request , f"{product_name} Is Saved Successfully..!")
        return render(request, "product/sell_product.html", context = context)
    else:
        messages.warning(request, '🤦‍♂️To add product, you should 🙋‍♂️sign in!')
        return render(request , 'accounts/login.html')
