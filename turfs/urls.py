# turfs/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.turfs_view, name='turfs'),
    path('turf_details/<int:turf_id>/', views.turf_details, name='turf_details'),
    path('search/', views.search_turfs, name='search_turfs'),
    path('book_turf/<int:turf_id>/', views.book_turf, name='book-turf'),

    path('turfs/turf_details/<int:turf_id>/', views.turf_details, name='turf-details'),  # Adjust the URL as needed
    path('turf/<int:turf_id>/write-review/', views.write_review, name='write_review'),

    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('confirm_delete_review/<int:review_id>/', views.confirm_delete_review, name='confirm_delete_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
]
