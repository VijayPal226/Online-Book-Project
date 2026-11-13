# adminapp/views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib.auth.models import User

# =========================
# Admin Login
# =========================

def adminlogin(request):

    return render(request,
        "adminapp/admin-login.html")


# =========================
# Dashboard
# =========================


@login_required
@user_passes_test(lambda u: u.is_superuser)
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

def addbook(request):

    return render(request,
        "adminapp/add-book.html")


# =========================
# Manage Books
# =========================

def managebooks(request):

    return render(request,
        "adminapp/manage-books.html")


# =========================
# Edit Book
# =========================

def editbook(request, id):

    return render(request,
        "adminapp/edit-book.html")


# =========================
# Categories
# =========================

def categories(request):

    return render(request,
        "adminapp/categories.html")


# =========================
# Authors
# =========================

def authors(request):

    return render(request,
        "adminapp/authors.html")


# =========================
# Manage Users
# =========================

def manageusers(request):

    return render(request,
        "adminapp/manage-users.html")


# =========================
# Orders
# =========================

def orders(request):

    return render(request,
        "adminapp/orders.html")


# =========================
# Payments
# =========================

def payments(request):

    return render(request,
        "adminapp/payments.html")


# =========================
# Reviews
# =========================

def reviews(request):

    return render(request,
        "adminapp/reviews.html")


# =========================
# Reports
# =========================

def reports(request):

    return render(request,
        "adminapp/reports.html")


# =========================
# Banners
# =========================

def banners(request):

    return render(request,
        "adminapp/banners.html")


# =========================
# Settings
# =========================

def settings(request):

    return render(request,
        "adminapp/settings.html")


# =========================
# Admin Logout
# =========================

def adminlogout(request):

    return render(request,
        "adminapp/admin-login.html")