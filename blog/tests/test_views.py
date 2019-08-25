from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q

from blog.tests.mixins import TestDataMixin
from blog.models import PERM,Comment


class BlogListViewTest(TestDataMixin, TestCase):
    def setUp(self):
        self.url = reverse('blog:blog')
        self.response = self.client.get(self.url)

    def test_can_get_page(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_correct_template(self):
        self.assertTemplateUsed(self.response, 'blog/index.html')
    
    def test_pagination_is_five(self):
        context = self.response.context
        self.assertTrue(context['is_paginated'])
        self.assertEqual(context['is_paginated'], True)
        self.assertEqual(len(context['blogs']), 5)
    
    def test_second_page(self):
        response = self.client.get(reverse('blog:blog') + '?page=2')
        context = response.context
        self.assertTrue(context['is_paginated'])
        self.assertEqual(context['is_paginated'], True)
        self.assertEqual(len(context['blogs']), 2)


class BlogDetailViewTest(TestDataMixin, TestCase):
    def setUp(self):
        self.url = reverse('blog:detail', args=[self.blog1.slug])
        self.response = self.client.get(self.url)
    
    def test_can_get(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_renders_correct_template(self):
        self.assertTemplateUsed(self.response, 'blog/detail.html')
    
    def test_context_is_blog(self):
        blog = self.response.context['blog']
        self.assertIsNotNone(blog)
        self.assertEqual(blog.title, self.blog1.title)
        self.assertEqual(blog.content, self.blog1.content)


class TestBloggerListView(TestDataMixin, TestCase):
    def setUp(self):
        self.url = reverse('blog:bloggers')
        self.response = self.client.get(self.url)
        self.bloggers = get_user_model().objects.filter(Q(user_permissions=PERM) | Q(is_superuser=True)).distinct()
    
    def test_can_get(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_renders_correct_template(self):
        self.assertTemplateUsed(self.response, 'blog/bloggers.html')
    
    def test_bloggers_in_context(self):
        bloggers = self.response.context['bloggers']
        for blogger in self.bloggers:
            self.assertTrue(blogger in bloggers)


class TestBloggerDetailView(TestDataMixin, TestCase):
    def setUp(self):
        self.url = reverse('blog:blogger', kwargs={'pk': self.user.pk})
        self.response = self.client.get(self.url)
    
    def test_can_get(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_blogger_in_context(self):
        blogger = self.response.context['blogger']
        self.assertEqual(blogger.bio, self.user.bio)
        self.assertEqual(blogger.blogs, self.user.blogs)


class TestCommentCreateView(TestDataMixin, TestCase):
    def setUp(self):
        self.url = reverse('blog:create_comment', kwargs={'slug': self.blog1.slug})
    
    def authenticated_client(self):
        client = Client()
        client.login(username='commenter', password='12345')
        return client
    
    def test_anonymous_user_cannot_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    
    def test_authenticated_user_can_get(self):
        client = self.authenticated_client()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_authenticated_user_can_post(self):
        client = self.authenticated_client()
        count = self.blog1.comments.count()
        response = client.post(self.url, data={'content': 'z'*256}, follow=True)
        self.assertRedirects(response, self.blog1.get_absolute_url())
        self.assertEqual(self.blog1.comments.count(), count + 1)
    
    def test_authenticated_user_cannot_post_too_big(self):
        client = self.authenticated_client()
        count = self.blog1.comments.count()
        response = client.post(self.url, data={'content': 'z'*1025}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.blog1.comments.count(), count)

    def test_anonymous_user_cannot_post(self):
        count = self.blog1.comments.count()
        response = self.client.post(self.url, data={'content': 'z'*256}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.blog1.comments.count(), count)


        