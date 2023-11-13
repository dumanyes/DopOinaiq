from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products_view, name='products'),
    path('products/<int:product_id>/', views.product_details, name='product_details'),
    path('products/search/', views.search_products, name='search_products'),
    path('products/add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('products/cart/', views.view_cart, name='cart'),
    path('products/remove-from-cart/<int:order_product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('products/checkout/', views.checkout, name='checkout'),
    path('update-cart/<int:order_product_id>/', views.update_cart, name='update_cart'),


    # path('product/<int:product_id>/write-review/', views.write_review, name='write_review'),
    #
    # path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    # path('confirm_delete_review/<int:review_id>/', views.confirm_delete_review, name='confirm_delete_review'),
    # path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),

    # path('product/<int:product_id>/write-review/', views.write_review, name='write_review'),
    #
    # # Edit an existing review
    # path('product/review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    #
    # # Confirm and delete a review
    # path('product/review/<int:review_id>/confirm-delete/', views.confirm_delete_review, name='confirm_delete_review'),
    #
    # # Delete a review
    # path('product/review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]
