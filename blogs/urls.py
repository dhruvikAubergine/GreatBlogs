from django.urls import path
from .views import BlogList, BlogDetail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('list/', BlogList.as_view(), name='blog-list'),
    path('<int:pk>/', BlogDetail.as_view(), name='blog-details'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
