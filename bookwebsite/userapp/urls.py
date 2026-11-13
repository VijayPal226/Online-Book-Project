from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard_view, name='user_dashboard'),

    path('profile/', views.user_profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    path('change-password/', views.change_password_view, name='change_password'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('otp-verification/', views.otp_verification_view, name='otp_verification'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),

    path('address/', views.address_view, name='address'),
    path('delete-account/', views.delete_account_view, name='delete_account'),

    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_wishlist_view, name='remove_wishlist'),

    path('my-books/', views.my_books_view, name='my_books'),
    path('downloads/', views.downloads_view, name='downloads'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('settings/', views.settings_view, name='settings'),
    path('support/', views.support_view, name='support'),
    path('reviews/', views.reviews_view, name='reviews'),

    path('payment-methods/', views.payment_methods_view, name='payment_methods'),
    path('payment-history/', views.payment_history_view, name='payment_history'),
    path('subscription/', views.subscription_view, name='subscription'),
]
