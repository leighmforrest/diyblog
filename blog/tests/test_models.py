from django.test import TestCase
from .mixins import TestDataMixin
from django.utils.text import slugify

from blog.models import Blog, Comment


class TestBlogModel(TestDataMixin, TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(blogger=self.user, content='x'*125, title='test_blog')

    def test_can_create(self):
        self.assertIsNotNone(self.blog)
        
    def test_slug_saved(self):
        slug = slugify(self.blog1.title)
        self.assertEqual(slug, self.blog1.slug)
    
    def test_blog_fields(self):
        self.assertIsNotNone(self.blog1.content)
        self.assertIsNotNone(self.blog1.created_at)
        self.assertIsNotNone(self.blog1.updated_at)
        self.assertEqual(self.user, self.blog1.blogger)
    
    def test_string(self):
        self.assertEqual(self.blog.title, str(self.blog))
    
    def test_get_absolute_url(self):
        slug = self.blog.slug
        url = f'/blog/{slug}/'
        self.assertEqual(url, self.blog.get_absolute_url())


class TestCommentModel(TestDataMixin, TestCase):
    def setUp(self):
        self.comment = Comment.objects.create(user=self.commenter, content='y'*256, blog=self.blog1)
    
    def test_can_create(self):
        self.assertIsNotNone(self.comment)
    
    def test_fields(self):
        self.assertEqual(self.blog1.comments.get(pk=self.comment.pk), self.comment)
        self.assertEqual(self.blog1, self.comment.blog)
        self.assertIsNotNone(self.comment.created_at)
        self.assertIsNotNone(self.comment.updated_at)
    
    def test_long_string(self):
        self.assertEqual(self.comment.content[:75] + '...', str(self.comment))
    
    def test_short_string(self):
        content = 'Z'*25
        self.comment.content = content
        self.assertEqual(content, str(self.comment))
