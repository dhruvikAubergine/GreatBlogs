from django.db import models
from accounts.models import User


class Blog(models.Model):
    def nameFile(instance, filename):
        return '/'.join(['images', str(instance.title), filename])

    title = models.CharField(max_length=100, blank=True, default='')
    picture = models.ImageField(upload_to=nameFile, blank=True)
    content = models.TextField(blank=True, default='')
    author = models.ForeignKey(User, related_name='blogs', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title
