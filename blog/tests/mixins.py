from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from blog.models import Blog, Comment


class TestDataMixin:
    @classmethod
    def setUpTestData(cls):
        # create test users
        cls.user = get_user_model().objects.create_user(username='testuser', password='12345')
        cls.user1 = get_user_model().objects.create_user(username='scrubby', password='12345')
        cls.commenter = get_user_model().objects.create_user(username='commenter', password='12345')

        # give bloggers blogger permission
        permission = Permission.objects.get(name='create update and delete blogs')
        cls.user.user_permissions.add(permission)
        cls.user1.user_permissions.add(permission)
        cls.user1.save()
        cls.user.save()

        # create blog posts
        cls.blog1 = Blog.objects.create(blogger=cls.user, content='x'*128, title='blog post')
        cls.blog2 = Blog.objects.create(blogger=cls.user, content='x'*128, title='blog post2')

        for _ in range(5):
            Blog.objects.create(blogger=cls.user1, content='x'*128, title='y'*64)

        # create comments
        Comment.objects.create(blog=cls.blog1, content='x'*128, user=cls.commenter)
        Comment.objects.create(blog=cls.blog2, content='x'*128, user=cls.user1)

