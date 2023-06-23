from django.urls import path
from products.views import get_products, insert_product


urlpatterns = [
    path('<slug>/' , get_products, name="get_products"),
    path('sell_product', insert_product, name="sell_product")
]
