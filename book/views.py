# book/views.py
from django.shortcuts import render
from rest_framework.views import APIView

class Book(APIView):
    def get(self, request):
        return render(request, 'book/recommend_book.html')
