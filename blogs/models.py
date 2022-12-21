from django.db import models
from accounts.models import User


class Blog(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True, default='')
    author = models.ForeignKey(User, related_name='blogs', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title
