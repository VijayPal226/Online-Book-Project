# adminapp/models.py

from django.db import models


# =========================
# Category Model
# =========================

class Category(models.Model):

    category_name = models.CharField(
        max_length=100)

    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):

        return self.category_name


# =========================
# Author Model
# =========================

class Author(models.Model):

    author_name = models.CharField(
        max_length=100)

    author_email = models.EmailField()

    author_image = models.ImageField(
        upload_to='authors/')

    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):

        return self.author_name


# =========================
# Banner Model
# =========================

class Banner(models.Model):

    banner_title = models.CharField(
        max_length=200)

    banner_image = models.ImageField(
        upload_to='banners/')

    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):

        return self.banner_title


# =========================
# Book Model
# =========================

class Book(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE)

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE)

    book_name = models.CharField(
        max_length=200)

    book_price = models.IntegerField()

    book_quantity = models.IntegerField()

    book_description = models.TextField()

    book_image = models.ImageField(
        upload_to='books/')

    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):

        return self.book_name


# =========================
# User Model
# =========================

class User(models.Model):

    name = models.CharField(
        max_length=100)

    email = models.EmailField(
        unique=True)

    contactno = models.CharField(
        max_length=15)

    address = models.TextField()

    password = models.CharField(
        max_length=100)

    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):

        return self.name


# =========================
# Cart Model
# =========================

class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE)

    quantity = models.IntegerField(
        default=1)

    total_price = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):

        return self.user.name


# =========================
# Wishlist Model
# =========================

class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE)

    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):

        return self.user.name


# =========================
# Order Model
# =========================

class Order(models.Model):

    STATUS_CHOICES = (

        ('Pending', 'Pending'),

        ('Completed', 'Completed'),

        ('Cancelled', 'Cancelled'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE)

    quantity = models.IntegerField()

    total_price = models.IntegerField()

    order_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending')

    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):

        return self.user.name


# =========================
# Payment Model
# =========================

class Payment(models.Model):

    PAYMENT_CHOICES = (

        ('COD', 'COD'),

        ('UPI', 'UPI'),

        ('Card', 'Card'),

    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES)

    payment_amount = models.IntegerField()

    payment_status = models.CharField(
        max_length=20)

    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):

        return self.payment_method


# =========================
# Review Model
# =========================

class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE)

    review_message = models.TextField()

    rating = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):

        return self.user.name