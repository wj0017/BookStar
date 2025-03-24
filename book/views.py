# book/views.py
from django.shortcuts import render
from rest_framework.views import APIView  # REST APIView 사용 시

class Book(APIView):  # 클래스 기반 뷰 (CBV)
    def get(self, request):
        return render(request, 'book/recommend_book.html')
