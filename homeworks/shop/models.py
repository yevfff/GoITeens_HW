from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin_user = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_admin_user:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/')
    new = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_name} ({self.stock} шт)"


class BasketItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket')
    items = models.ManyToManyField(BasketItem)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    def __str__(self):
        return f"Кошик: {self.user.username}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def total_amount(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    def __str__(self):
        return f"Замовлення #{self.id} від {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity} (Замовлення #{self.order.id})"


# 3 моделі для дз:

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Профіль {self.user.username}"


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    products = models.ManyToManyField(Product, related_name="suppliers", blank=True)  # Тут зробимо ManyToMany

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')  # один користувач → багато списків
    products = models.ManyToManyField(Product, related_name='in_wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Список бажаного {self.user.username} (#{self.id})"
