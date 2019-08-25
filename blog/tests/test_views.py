from django.test import TestCase
from django.urls import reverse

from blog.tests.mixins import TestDataMixin


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
