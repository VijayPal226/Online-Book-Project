from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# ================= 1. LOGIN =================
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_view(request):

    # agar user already login hai
    if request.user.is_authenticated:

        if request.user.is_superuser:
            return redirect('admin_dashboard')

        return redirect('user_dashboard')

    # login form submit
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # admin login
            if user.is_superuser:
                return redirect('admin_dashboard')

            # normal user login
            return redirect('user_dashboard')

        else:
            messages.error(request, "Invalid Username or Password")

    # IMPORTANT
    return render(request, 'userapp/login.html')

# ================= 2. SIGNUP =================

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

    user = User.objects.create_user(
    username=username,
    email=email,
    password=password1
    )

    user.save()

# User ko automatic login kara do
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
    context = {
       'user': request.user,
    }
    return render(request, "userapp/dashboard.html", context )

# ================= 5. USER PROFILE =================
@login_required
def user_profile_view(request):
    return render(request, "userapp/profile.html")


# ================= 6. EDIT PROFILE =================
@login_required
def edit_profile_view(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
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

        user.set_password(new1)
        user.save()

        messages.success(request, "Password changed successfully")
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
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "userapp/otp-verification.html")


# ================= 10. ADDRESS =================
@login_required
def address_view(request):
    return render(request, "userapp/address.html")


# ================= 11. DELETE ACCOUNT =================
@login_required
def delete_account_view(request):
    if request.method == "POST":
        request.user.delete()
        messages.success(request, "Account deleted successfully")
        return redirect('signup')

    return render(request, "userapp/delete_account.html")


# ================= 12. WISHLIST =================
@login_required
def wishlist_view(request):
    return render(request, "userapp/wishlist.html")


# ================= 13. MY BOOKS =================
@login_required
def my_books_view(request):
    return render(request, "userapp/my-books.html")


# ================= 14. DOWNLOADS =================
@login_required
def downloads_view(request):
    return render(request, "userapp/downloads.html")


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
    return render(request, "userapp/reviews.html")


# ================= 19. PAYMENT METHODS =================
@login_required
def payment_methods_view(request):
    return render(request, "userapp/payment_methods.html")


# ================= 20. PAYMENT HISTORY =================
@login_required
def payment_history_view(request):
    return render(request, "userapp/payment_history.html")


# ================= 21. SUBSCRIPTION =================
@login_required
def subscription_view(request):
    return render(request, "userapp/subscription.html")