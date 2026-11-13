# adminapp/urls.py

from django.urls import path
from . import views

urlpatterns = [

    # Admin Login
    path('admin-login/', views.adminlogin,name='adminlogin'),

    # Dashboard
    path('dashboard/', views.dashboard,name='admin_dashboard'),

    # Add Book
    path('add-book/', views.addbook,name='addbook'),

    # Manage Books
    path('manage-books/', views.managebooks,name='managebooks'),

    # Edit Book
    path('edit-book/<int:id>/', views.editbook,name='editbook'),

    # Categories
    path('categories/', views.categories,name='categories'),

    # Authors
    path('authors/', views.authors,name='authors'),

    # Manage Users
    path('manage-users/', views.manageusers,name='manageusers'),

    # Orders
    path('orders/', views.orders,name='orders'),

    # Payments
    path('payments/', views.payments,name='payments'),

    # Reviews
    path('reviews/', views.reviews,name='reviews'),

    # Reports
    path('reports/', views.reports,name='reports'),

    # Banners
    path('banners/', views.banners,name='banners'),

    # Settings
    path('settings/', views.settings,name='settings'),

    # Logout
    path('admin-logout/',views.adminlogout,name='adminlogout'),

]