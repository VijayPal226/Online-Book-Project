from django.db import models
from django.contrib.auth.models import User
from mainapp.models import Book


# ================= ADDRESS MODEL =================
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)

    address_line = models.TextField()

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    postal_code = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# ================= WISHLIST MODEL =================
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Wishlist"


# ================= ORDER MODEL =================
class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=100)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


# ================= ORDER ITEM MODEL =================
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.book.title


# ================= REVIEW MODEL =================
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    rating = models.PositiveIntegerField(default=5)

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username