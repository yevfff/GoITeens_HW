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
