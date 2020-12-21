from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="dada.jpg",null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length =20, null=True)
    email = models.CharField(max_length=30, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
             ('Outdoor', 'Outdoor'),
             ('Indoor', 'Indoor')    
             )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(max_length =20, null=True)
    category = models.CharField(max_length=30, null=True, choices=CATEGORY)
    description = models.CharField(max_length=300, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
             ('Pending', 'Pending'),
             ('Out for delivery', 'Out for delivery'),
             ('Delivered', 'Delivered')    
             )
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    notes = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.product.name

