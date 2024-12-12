from django.contrib import admin

from .models import Book, Cart, CartItem

admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(CartItem)