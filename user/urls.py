from django.urls import path
from .views import Login, Join, Logout

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('join/', Join.as_view(), name='join'),
    path('logout/', Logout.as_view(), name='logout'),
]