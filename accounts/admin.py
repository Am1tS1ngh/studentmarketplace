from django.contrib import admin

# Register your models here.
from .models import Profile, CartItems , Cart

admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItems)
