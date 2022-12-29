from rest_framework import status
from rest_framework.response import Response

from blogs.models import Blog
from .serializers import BlogSerializer
from .pagination import BlogListPagination
from rest_framework import permissions, filters
from .permissions import IsAuthorOrReadOnly
from rest_framework.views import APIView


# For get a blog list with pagination and create a new blog
class BlogList(APIView):
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "author__username"]
    pagination_class = BlogListPagination
    queryset = Blog.objects.all().order_by("-created_on")

    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request):
        queryset = self.queryset.order_by("-created_on")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(
                [{"success": "New blog created successfully"}, serializer.data],
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Something went wrong, Please try again"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# For get particular blog details, update and delete
class BlogDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = BlogSerializer

    def get(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {"error": "Something went wrong, Please try again"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        blog.delete()
        return Response(
            {"success": "Blog is deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

