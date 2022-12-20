from rest_framework.pagination import PageNumberPagination


class BlogListPagination(PageNumberPagination):
    page_size = 3