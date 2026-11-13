# adminapp/views.py

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# =========================
# Admin Required Decorator
# =========================

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('user_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# =========================
# Admin Login
# =========================

def adminlogin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # email se bhi login allowed hai
        if '@' in username:
            user_obj = User.objects.filter(email__iexact=username).first()
            if user_obj:
                username = user_obj.username

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')

        if user is not None:
            messages.error(request, "This account does not have admin access")
        else:
            messages.error(request, "Invalid username or password")

    return render(request,
        "adminapp/admin-login.html")


# =========================
# Dashboard
# =========================

@admin_required
def dashboard(request):

    total_users = User.objects.filter(
        is_superuser=False
    ).count()

    context = {
        "total_users": total_users,
    }

    return render(
        request,
        "adminapp/dashboard.html",
        context
    )


# =========================
# Add Book
# =========================

@admin_required
def addbook(request):

    return render(request,
        "adminapp/add-book.html")


# =========================
# Manage Books
# =========================

@admin_required
def managebooks(request):

    return render(request,
        "adminapp/manage-books.html")


# =========================
# Edit Book
# =========================

@admin_required
def editbook(request, id):

    return render(request,
        "adminapp/edit-book.html")


# =========================
# Categories
# =========================

@admin_required
def categories(request):

    return render(request,
        "adminapp/categories.html")


# =========================
# Authors
# =========================

@admin_required
def authors(request):

    return render(request,
        "adminapp/authors.html")


# =========================
# Manage Users
# =========================

@admin_required
def manageusers(request):

    return render(request,
        "adminapp/manage-users.html")


# =========================
# Orders
# =========================

@admin_required
def orders(request):

    return render(request,
        "adminapp/orders.html")


# =========================
# Payments
# =========================

@admin_required
def payments(request):

    return render(request,
        "adminapp/payments.html")


# =========================
# Reviews
# =========================

@admin_required
def reviews(request):

    return render(request,
        "adminapp/reviews.html")


# =========================
# Reports
# =========================

@admin_required
def reports(request):

    return render(request,
        "adminapp/reports.html")


# =========================
# Banners
# =========================

@admin_required
def banners(request):

    return render(request,
        "adminapp/banners.html")


# =========================
# Settings
# =========================

@admin_required
def settings(request):

    return render(request,
        "adminapp/settings.html")


# =========================
# Admin Logout
# =========================

def adminlogout(request):
    logout(request)
    return redirect('adminlogin')
