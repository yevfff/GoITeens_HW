from django.contrib import admin
from .models import User, Category, Product, BasketItem, Basket, Order, OrderItem, Profile, Supplier, Wishlist, FeaturedCollection

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'category', 'price', 'stock', 'new')
    search_fields = ('product_name',)
    list_filter = ('category', 'new')

@admin.register(FeaturedCollection)
class FeaturedCollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    filter_horizontal = ('products',)

admin.site.register(Category)
admin.site.register(User)
admin.site.register(BasketItem)
admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(Supplier)
admin.site.register(Wishlist)
