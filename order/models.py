from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )


    PAYMENT_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI Demo'),
        ('CARD', 'Credit/Debit Card Demo'),
    )



    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )


    full_name = models.CharField(
        max_length=100,
        default=""
    )


    phone = models.CharField(
        max_length=15,
        default=""
    )


    address = models.TextField(
        default=""
    )


    city = models.CharField(
        max_length=100,
        default=""
    )


    pincode = models.CharField(
        max_length=10,
        default=""
    )


    quantity = models.IntegerField(
        default=1
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )


    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="COD"
    )


    ordered_at = models.DateTimeField(
        auto_now_add=True
    )



    @property
    def total_price(self):

        return self.product.price * self.quantity



    def __str__(self):

        return f"{self.user.username} - {self.product.name}"