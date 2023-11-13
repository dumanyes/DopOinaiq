from django.contrib import admin
from .models import Product, ProductImage, OrderProduct, Order, ProductReview


# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ProductReview)
