from django.db import models
from django.contrib.auth.models import User


# ================= CATEGORY MODEL =================
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name


# ================= AUTHOR MODEL =================
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='authors/', blank=True, null=True)

    def __str__(self):
        return self.name


# ================= BOOK MODEL =================
class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    image = models.ImageField(upload_to='books/')
    pdf_file = models.FileField(upload_to='books/pdfs/', blank=True, null=True)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    stock = models.PositiveIntegerField(default=1)

    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ================= CONTACT MODEL =================
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ================= CART MODEL =================
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"