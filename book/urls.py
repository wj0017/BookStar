# book/urls.py
from django.urls import path
from .views import Book

urlpatterns = [
    path('', Book.as_view(), name='book_page'),
]