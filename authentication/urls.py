from django.urls import path
from .views import UserRegister, UserLogin, LogoutView

urlpatterns = [
    path('register', UserRegister.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
