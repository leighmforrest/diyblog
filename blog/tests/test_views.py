from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Q

from blog.tests.mixins import TestDataMixin
from blog.models import Comment


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
        permission = Permission.objects.get(name='create update and delete blogs')
        self.bloggers = get_user_model().objects.filter(Q(user_permissions=permission) | Q(is_superuser=True)).distinct()
    
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
    
    def test_template_used(self):
        client = self.authenticated_client()
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed('blog/comment_form.html')
    
    def test_authenticated_user_can_post(self):
        client = self.authenticated_client()
        count = self.blog1.comments.count()
        response = client.post(self.url, data={'content': 'z'*256}, follow=True)
        self.assertRedirects(response, self.blog1.get_absolute_url())
        self.assertEqual(self.blog1.comments.count(), count + 1)
    
    def test_create_success_message(self):
        expected_message = 'The comment has been created.'
        client = self.authenticated_client()
        response = client.post(self.url, data={'content': 'z'*256}, follow=True)

        self.assertIn(expected_message.encode('utf-8'), response.content)

        messages = list(response.context['messages'])
        self.assertIn(expected_message.encode('utf-8'), response.content)

        for message in messages:
            self.assertEqual(str(message), expected_message)
    
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


class BlogCommentUpdateViewTest(TestDataMixin, TestCase):
    def setUp(self):
        self.comment = self.blog1.comments.get(user=self.commenter)
        self.url = reverse('blog:update_comment', kwargs={'pk': self.comment.pk})
    
    def authenticated_client(self):
        client = Client()
        client.login(username='commenter', password='12345')
        return client

    def test_commenter_can_get(self):
        client = self.authenticated_client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_non_commenter_cannot_get(self):
        client = Client()
        client.login(username='user1', password='12345')
        response = client.get(self.url)
        self.assertEqual(response.status_code, 403)
    
    def test_anonymous_user_cannot_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_template_used(self):
        client = self.authenticated_client()
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed('blog/comment_form.html')
    
    def test_commenter_can_update(self):
        content = 'abc'*32
        client = self.authenticated_client()
        response = client.post(self.url, data={'content': content})
        comment = Comment.objects.get(pk=self.comment.pk)
        self.assertEqual(comment.content, content)
    
    def test_update_success_message(self):
        expected_message = 'The blog has been updated.'
        content = 'abc'*32
        client = self.authenticated_client()
        response = client.post(self.url, data={'content': content}, follow=True)

        self.assertIn(expected_message.encode('utf-8'), response.content)

        messages = list(response.context['messages'])
        self.assertIn(expected_message.encode('utf-8'), response.content)

        for message in messages:
            self.assertEqual(str(message), expected_message)
    
    def test_non_commenter_cannot_update(self):
        client = Client()
        client.login(username='user1', password='12345')
        response = client.get(self.url, data={'content': 'abc'})
        self.assertEqual(response.status_code, 403)


class BlogCommentDeleteViewTest(TestDataMixin, TestCase):
    def setUp(self):
        self.comment = self.blog1.comments.get(user=self.commenter)
        self.url = reverse('blog:delete_comment', kwargs={'pk': self.comment.pk})
    
    def authenticated_client(self):
        client = Client()
        client.login(username='commenter', password='12345')
        return client

    def test_commenter_can_get(self):
        client = self.authenticated_client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_non_commenter_cannot_get(self):
        client = Client()
        client.login(username='user1', password='12345')
        response = client.get(self.url)
        self.assertEqual(response.status_code, 403)
    
    def test_anonymous_user_cannot_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_template_used(self):
        client = self.authenticated_client()
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed('blog/delete.html')
    
    def test_commenter_can_delete(self):
        client = self.authenticated_client()
        response = client.post(self.url)
        comment = Comment.objects.filter(pk=self.comment.pk)
        self.assertEqual(len(comment), 0)
    
    def test_delete_success_message(self):
        expected_message = 'The comment has been deleted.'
        client = self.authenticated_client()
        response = client.post(self.url, follow=True)

        self.assertIn(expected_message.encode('utf-8'), response.content)

        messages = list(response.context['messages'])
        self.assertIn(expected_message.encode('utf-8'), response.content)

        for message in messages:
            self.assertEqual(str(message), expected_message)
    
    def test_non_commenter_cannot_delete(self):
        client = Client()
        client.login(username='user1', password='12345')
        response = client.get(self.url, data={})
        self.assertEqual(response.status_code, 403)


