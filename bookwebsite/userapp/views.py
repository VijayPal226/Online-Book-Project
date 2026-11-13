from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from mainapp.models import Book
from .models import Address, Wishlist, Order, OrderItem, Review


# ================= 1. LOGIN =================
def login_view(request):

    # agar user already login hai
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('user_dashboard')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # "Username or Email" — email se bhi login allowed hai
        if '@' in username:
            user_obj = User.objects.filter(email__iexact=username).first()
            if user_obj:
                username = user_obj.username

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')

            return redirect('user_dashboard')

        messages.error(request, "Invalid Username or Password")

    return render(request, 'userapp/login.html')


# ================= 2. SIGNUP =================
def signup_view(request):

    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        # Basic validation
        if not username or not email or not password1:
            messages.error(request, "Please fill all required fields")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        try:
            validate_password(password1)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )

        login(request, user)
        messages.success(request, "Account created successfully")
        return redirect('user_dashboard')

    return render(request, "userapp/signup.html")


# ================= 3. LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('login')


# ================= 4. DASHBOARD =================
@login_required
def dashboard_view(request):
    orders = Order.objects.filter(user=request.user)

    context = {
        'user': request.user,
        'total_orders': orders.count(),
        'total_products': OrderItem.objects.filter(order__user=request.user).count(),
        'total_revenue': orders.aggregate(total=models.Sum('total_price'))['total'] or 0,
        'recent_orders': orders.order_by('-ordered_at')[:5],
    }
    return render(request, "userapp/dashboard.html", context)


# ================= 5. USER PROFILE =================
@login_required
def user_profile_view(request):
    return render(request, "userapp/profile.html")


# ================= 6. EDIT PROFILE =================
@login_required
def edit_profile_view(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username", user.username).strip()
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.email = request.POST.get("email", "")

        # Username / email uniqueness check (excluding self)
        if User.objects.filter(username=user.username).exclude(id=user.id).exists():
            messages.error(request, "Username already taken")
            return redirect('edit_profile')

        user.save()

        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    return render(request, "userapp/edit-profile.html")


# ================= 7. CHANGE PASSWORD =================
@login_required
def change_password_view(request):
    if request.method == "POST":
        user = request.user
        old = request.POST.get("old_password")
        new1 = request.POST.get("new_password1")
        new2 = request.POST.get("new_password2")

        if not user.check_password(old):
            messages.error(request, "Old password incorrect")
            return redirect('change_password')

        if new1 != new2:
            messages.error(request, "Passwords do not match")
            return redirect('change_password')

        try:
            validate_password(new1, user=user)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('change_password')

        user.set_password(new1)
        user.save()

        # password change ke baad dobara login zaroori
        logout(request)
        messages.success(request, "Password changed successfully. Please login again.")
        return redirect('login')

    return render(request, "userapp/change_password.html")


# ================= 8. FORGOT PASSWORD =================
def forgot_password_view(request):
    if request.method == "POST":
        messages.success(request, "OTP sent to email (demo)")
        return redirect('otp_verification')

    return render(request, "userapp/forgot-password.html")


# ================= 9. OTP VERIFICATION =================
def otp_verification_view(request):
    if request.method == "POST":
        otp = request.POST.get("otp")

        if otp == "123456":
            messages.success(request, "OTP verified successfully")
            return redirect('login')

        messages.error(request, "Invalid OTP")

    return render(request, "userapp/otp-verification.html")


# ================= 9b. RESEND OTP =================
def resend_otp_view(request):
    messages.success(request, "OTP resent successfully (demo)")
    return redirect('otp_verification')


# ================= 10. ADDRESS =================
@login_required
def address_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address_line = request.POST.get("address_line", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        country = request.POST.get("country", "India").strip() or "India"
        postal_code = request.POST.get("postal_code", "").strip()

        if not all([full_name, phone, address_line, city, state, postal_code]):
            messages.error(request, "Please fill all address fields")
        else:
            Address.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                address_line=address_line,
                city=city,
                state=state,
                country=country,
                postal_code=postal_code,
            )
            messages.success(request, "Address saved successfully")

        return redirect('address')

    addresses = Address.objects.filter(user=request.user).order_by('-created_at')
    context = {'addresses': addresses}
    return render(request, "userapp/address.html", context)


# ================= 11. DELETE ACCOUNT =================
@login_required
def delete_account_view(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = request.user

        if not user.check_password(password):
            messages.error(request, "Incorrect password")
            return redirect('delete_account')

        user.delete()
        messages.success(request, "Account deleted successfully")
        return redirect('signup')

    return render(request, "userapp/delete_account.html")


# ================= 12. WISHLIST =================
@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user).select_related('book')
    context = {'wishlist': wishlist}
    return render(request, "userapp/wishlist.html", context)


# ================= 12b. REMOVE FROM WISHLIST =================
@login_required
def remove_wishlist_view(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id, user=request.user)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Removed from wishlist")

    return redirect('wishlist')


# ================= 13. MY BOOKS =================
@login_required
def my_books_view(request):
    # purchased books via order items
    book_ids = OrderItem.objects.filter(
        order__user=request.user
    ).values_list('book_id', flat=True)

    books = Book.objects.filter(id__in=book_ids).distinct()

    context = {'books': books}
    return render(request, "userapp/my-books.html", context)


# ================= 14. DOWNLOADS =================
@login_required
def downloads_view(request):
    book_ids = OrderItem.objects.filter(
        order__user=request.user
    ).values_list('book_id', flat=True)

    books = Book.objects.filter(
        id__in=book_ids,
        pdf_file__isnull=False
    ).exclude(pdf_file='').distinct()

    context = {'downloads': books}
    return render(request, "userapp/downloads.html", context)


# ================= 15. NOTIFICATIONS =================
@login_required
def notifications_view(request):
    return render(request, "userapp/notifications.html")


# ================= 16. SETTINGS =================
@login_required
def settings_view(request):
    return render(request, "userapp/settings.html")


# ================= 17. SUPPORT =================
@login_required
def support_view(request):
    if request.method == "POST":
        messages.success(request, "Support ticket submitted")
        return redirect('support')

    return render(request, "userapp/support.html")


# ================= 18. REVIEWS =================
@login_required
def reviews_view(request):
    reviews = Review.objects.filter(user=request.user).select_related('book')
    context = {'reviews': reviews}
    return render(request, "userapp/reviews.html", context)


# ================= 19. PAYMENT METHODS =================
@login_required
def payment_methods_view(request):
    if request.method == "POST":
        method = request.POST.get("method", "")
        if method:
            messages.success(request, f"{method} payment selected (demo)")
        return redirect('payment_methods')

    return render(request, "userapp/payment_methods.html")


# ================= 20. PAYMENT HISTORY =================
@login_required
def payment_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    context = {'orders': orders}
    return render(request, "userapp/purchase-history.html", context)


# ================= 21. SUBSCRIPTION =================
@login_required
def subscription_view(request):
    if request.method == "POST":
        plan = request.POST.get("plan", "")
        if plan:
            messages.success(request, f"{plan} plan selected (demo)")
        return redirect('subscription')

    return render(request, "userapp/subscription.html")
