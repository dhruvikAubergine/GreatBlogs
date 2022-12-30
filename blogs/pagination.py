from rest_framework.pagination import PageNumberPagination


class BlogListPagination(PageNumberPagination):
    # Blog list page size.
    page_size = 3