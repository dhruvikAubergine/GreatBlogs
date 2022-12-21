from django.contrib import admin
from django.urls import path, include
from .views import RegisterView, UserDetailView, UserListView, LoginView, VerifyEmailView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='ragister'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-verify/', VerifyEmailView.as_view(), name="email-verify"),
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),

]
