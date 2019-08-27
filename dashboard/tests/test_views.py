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