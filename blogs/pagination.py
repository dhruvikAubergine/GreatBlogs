from rest_framework.pagination import PageNumberPagination


# For blog list pagination
class BlogListPagination(PageNumberPagination):
    page_size = 3