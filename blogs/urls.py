from django.urls import path
from .views import BlogListView, BlogDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('list/', BlogListView.as_view(), name='blog-list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog-details'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
