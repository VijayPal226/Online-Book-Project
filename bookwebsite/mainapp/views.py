from django.shortcuts import render


def home(request):
    return render(request, 'mainapp/home.html')


def about(request):
    return render(request, 'mainapp/about.html')


def contact(request):
    return render(request, 'mainapp/contact.html')


def cart(request):
    return render(request, 'mainapp/cart.html')