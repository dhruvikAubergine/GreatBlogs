from django.contrib import admin
from django.urls import path, include
from .views import RegisterView,UserDetail, UserList
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterView.as_view(), name='ragister'),
    path('login/', obtain_auth_token, name='login'),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),

]
