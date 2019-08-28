from django.test import TestCase, Client
from blog.tests.mixins import TestDataMixin
from django.urls import reverse

from blog.models import Blog


class DashboardViewTest(TestDataMixin, TestCase):
    def setUp(self):
        self.url = reverse('dashboard:index')

        # make two more blogs
        for _ in range(2):
            Blog.objects.create(blogger=self.user1, content='x'*128, title='y'*64)

    def authenticated_client(self):
        client = Client()
        client.login(username=self.user1.username, password='12345')
        return client

    def test_auth_user_can_get(self):
        client = self.authenticated_client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_correct_template(self):
        client = self.authenticated_client()
        response = client.get(self.url)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_pagination_is_five(self):
        client = self.authenticated_client()
        response = client.get(self.url)
        context = response.context
        self.assertTrue(context['is_paginated'])
        self.assertEqual(context['is_paginated'], True)
        self.assertEqual(len(context['blogs']), 5)
    
    def test_second_page(self):
        client = self.authenticated_client()
        response = client.get(self.url + '?page=2')
        context = response.context
        self.assertTrue(context['is_paginated'])
        self.assertEqual(context['is_paginated'], True)
        self.assertEqual(len(context['blogs']), 2)


class BlogCreateViewTest(TestDataMixin, TestCase):
    def setUp(self):
        self.url = reverse('dashboard:create_blog')
        self.data = {'title': 'This is the title', 'content': 'abc'* 100}

    def authenticated_client(self):
        client = Client()
        client.login(username=self.user1.username, password='12345')
        return client
    
    def test_blogger_can_get(self):
        client = self.authenticated_client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_create_blog_in_template(self):
        client = self.authenticated_client()
        response = client.get(self.url)
        self.assertFalse(response.context['update'])
        self.assertTrue('<h1>Create Blog</h1>' in str(response.content))
    
    def test_create_success_message(self):
        expected_message = 'The blog has been created.'
        client = self.authenticated_client()
        response = client.post(self.url, data=self.data, follow=True)

        self.assertIn(expected_message.encode('utf-8'), response.content)

        messages = list(response.context['messages'])
        self.assertIn(expected_message.encode('utf-8'), response.content)

        for message in messages:
            self.assertEqual(str(message), expected_message)
    
    def test_anonymous_user_cannot_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    
    def test_blogger_can_post(self):
        count = self.user1.blogs.count()
        client = self.authenticated_client()
        response = client.post(self.url, data=self.data, follow=True)
        self.assertEqual(self.user1.blogs.count(), count + 1)
        self.assertRedirects(response, reverse('dashboard:index'), status_code=302)
    
    def test_non_blogger_cannot_post(self):
        client = Client()
        client.login(username="commenter", password='12345')
        response = client.post(self.url, data=self.data, follow=True)
        self.assertEqual(response.status_code, 403)
    
    def test_anonymous_user_cannot_post(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)


class BlogUpdateViewTest(TestDataMixin, TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(title='This is the title', content='abc'* 100, blogger=self.user1)
        self.url = reverse('dashboard:update_blog', kwargs={'slug': self.blog.slug})
        self.data = {'title': 'There is a new title', 'content': 'x'* 500}

    def authenticated_client(self):
        client = Client()
        client.login(username=self.user1.username, password='12345')
        return client
    
    def test_blogger_can_get(self):
        client = self.authenticated_client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_update_blog_in_template(self):
        client = self.authenticated_client()
        response = client.get(self.url)
        self.assertTrue(response.context['update'])
        self.assertTrue('<h1>Update Blog</h1>' in str(response.content))
    
    def test_aononymous_user_cannot_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
    
    def test_blogger_can_update(self):
        client = self.authenticated_client()
        response = client.post(self.url, data=self.data, follow=True)
        blog = Blog.objects.get(pk=self.blog.pk)
        self.assertTrue(blog.title, self.data['title'])
        self.assertTrue(blog.content, self.data['content'])
        self.assertRedirects(response, reverse('dashboard:index'), status_code=302)
    
    def test_update_success_message(self):
        expected_message = 'The blog has been updated.'
        client = self.authenticated_client()
        response = client.post(self.url, data=self.data, follow=True)

        self.assertIn(expected_message.encode('utf-8'), response.content)

        messages = list(response.context['messages'])
        self.assertIn(expected_message.encode('utf-8'), response.content)

        for message in messages:
            self.assertEqual(str(message), expected_message)
    
    def test_other_blogger_cannot_update(self):
        client = Client()
        client.login(username=self.user.username, password='12345')
        response = client.post(self.url, data=self.data, follow=True)
        self.assertEqual(response.status_code, 403)
    
    def test_non_blogger_cannot_update(self):
        client = Client()
        client.login(username="commenter", password='12345')
        response = client.post(self.url, data=self.data, follow=True)
        self.assertEqual(response.status_code, 403)
    
    def test_anonymous_user_cannot_update(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 403)


class BlogDeleteViewTest(TestDataMixin, TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(title='This is the title', content='abc'* 100, blogger=self.user1)
        self.url = reverse('dashboard:delete_blog', kwargs={'slug': self.blog.slug})

    def authenticated_client(self):
        client = Client()
        client.login(username=self.user1.username, password='12345')
        return client
    
    def test_blogger_cannot_get(self):
        client = self.authenticated_client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 405)
    
    def test_anonymous_user_cannot_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
    
    def test_blogger_can_delete(self):
        client = self.authenticated_client()
        response = client.post(self.url,  follow=True)
        self.assertRedirects(response, reverse('dashboard:index'), status_code=302)
    
    def test_update_success_message(self):
        expected_message = f"The blog has been deleted."
        client = self.authenticated_client()
        response = client.post(self.url, follow=True)

        self.assertIn(expected_message.encode('utf-8'), response.content)

        messages = list(response.context['messages'])
        self.assertIn(expected_message.encode('utf-8'), response.content)

        for message in messages:
            self.assertEqual(str(message), expected_message)
    
    def test_other_blogger_cannot_delete(self):
        client = Client()
        client.login(username=self.user.username, password='12345')
        response = client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 403)
    
    def test_non_blogger_cannot_delete(self):
        client = Client()
        client.login(username="commenter", password='12345')
        response = client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 403)
    
    def test_anonymous_user_cannot_delete(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

