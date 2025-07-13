from django.contrib import admin
from .models import User, Category, Product, BasketItem, Basket, Order, OrderItem

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(BasketItem)
admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(OrderItem)
