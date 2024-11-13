from django.db import models
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # New field for image

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Order by most recent
