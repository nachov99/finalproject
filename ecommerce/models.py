from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64, null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE = (
        ('Small','Small'),
        ('Medium','Medium'),
        ('Large','Large'),
    )
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=64, null=True)
    img_file = models.ImageField(null=True, blank=True)
    size = models.CharField(max_length=64, null=True, choices=SIZE, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.Category} - {self.name} - {self.size} - {self.price}"

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Initiated', 'Initiated'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ManyToManyField(Product)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=64, null=True, choices=STATUS, default='Pending')
    paid = models.BooleanField(default=False)
    def __str__(self):
        return f" Order Id: {self.id} - Customer: {self.customer} - Status: {self.status} - Paid: {self.paid} "

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
    msg = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.user_id} {self.product_id} {self.rating} {self.msg}"