from django.contrib import admin
from django.urls import path, include
from .views import BlogList, BlogDetail

urlpatterns = [
    # code omitted for brevity
    path('list/', BlogList.as_view(), name='blog-list'),
    path('<int:pk>/', BlogDetail.as_view(), name='blog-details'),
    path('api-auth/', include('rest_framework.urls')),
]
