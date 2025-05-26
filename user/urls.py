from django.urls import path
from .views import Login, Join, Logout, profile_view
from . import views

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('join/', Join.as_view(), name='join'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('onboarding/', views.onboarding_view, name='onboarding'),  # 추가
    path('onboarding/skip/', views.skip_onboarding_view, name='skip_onboarding'),  # 추가
]