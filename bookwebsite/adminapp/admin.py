from django.contrib import admin

from .models import *

admin.site.register(Category)

admin.site.register(Author)

admin.site.register(Banner)

admin.site.register(Book)

admin.site.register(User)

admin.site.register(Cart)

admin.site.register(Wishlist)

admin.site.register(Order)

admin.site.register(Payment)

admin.site.register(Review)