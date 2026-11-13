from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Book, Cart, ContactMessage
from userapp.models import Wishlist, Review


def home(request):
    books = Book.objects.filter(
        is_available=True
    ).select_related('category', 'author').order_by('-is_featured', '-created_at')[:12]

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list('book_id', flat=True)

    context = {
        'books': books,
        'wishlist_ids': list(wishlist_ids),
    }
    return render(request, 'mainapp/home.html', context)


def about(request):
    return render(request, 'mainapp/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message_text = request.POST.get("message", "").strip()

        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=f"Contact from {name}",
                message=message_text,
            )
            messages.success(request, "Message sent successfully. We will contact you soon.")
        else:
            messages.error(request, "Please fill all fields")

        return redirect('contact')

    return render(request, 'mainapp/contact.html')


def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_available=True)

    reviews = Review.objects.filter(book=book).select_related('user')

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user, book=book
        ).exists()

    context = {
        'book': book,
        'reviews': reviews,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'mainapp/book_details.html', context)


@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_available=True)

    if request.method == "POST":
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            book=book,
        )

        if created:
            messages.success(request, "Added to wishlist")
        else:
            wishlist_item.delete()
            messages.success(request, "Removed from wishlist")

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def addtocart(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_available=True)

    if request.method == "POST":
        if book.stock <= 0:
            messages.error(request, "This book is out of stock")
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'quantity': 1},
        )

        if not created:
            if cart_item.quantity >= book.stock:
                messages.warning(request, "Maximum stock reached for this book")
                return redirect('cart')
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, f"'{book.title}' added to cart")

    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Item removed from cart")

    return redirect('cart')


def cart(request):
    cart_items = Cart.objects.none()
    total = 0

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(
            user=request.user
        ).select_related('book')

        for item in cart_items:
            book = item.book
            item.unit_price = book.discount_price if book.discount_price else book.price
            item.line_total = item.unit_price * item.quantity
            total += item.line_total

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'mainapp/cart.html', context)
