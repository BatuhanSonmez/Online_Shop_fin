from django.contrib.auth.models import User
from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='seller', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_balance(self):
        items = self.items.filter(seller_paid=False, order__sellers__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.items.filter(seller_paid=True, order__sellers__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    order_by = models.IntegerField(default=0)

    class Meta:
        ordering = ['order_by']

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    sellers = models.ManyToManyField(Seller, related_name='orders')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, related_name='items', on_delete=models.CASCADE)
    seller_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id

    def get_total_price(self):
        return self.price * self.quantity

