from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify


class Blog(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blogger = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='blogs')
    slug = models.SlugField(max_length=100)

    class Meta:
        permissions = [
            ('blogger', 'create update and delete blogs'),
        ]
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content[:25]