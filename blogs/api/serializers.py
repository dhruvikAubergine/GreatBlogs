from rest_framework import serializers
from blogs.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Blog
        # fields = '__all__'
        fields = ['id', 'title', 'content', 'author', 'created_on']

