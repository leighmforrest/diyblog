from django.test import TestCase, Client
from django.urls import reverse
from blog.tests.mixins import TestDataMixin


class TestHomepageTest(TestDataMixin, TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('pages:home'))

    def test_can_get_page(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_correct_template_rendered(self):
        self.assertTemplateUsed(self.response, 'pages/index.html')
    
    def test_blogger_link_rendered(self):
        content = str(self.response.content)
        self.assertTrue('All Bloggers' in content)

    def test_login_links_rendered(self):
        response_text = str(self.response.content)
        self.assertTrue('Log In' in response_text)
        self.assertTrue('Log In with Gmail' in response_text)
    
    def test_authenticated_user_nav_links(self):
        client = Client()
        client.login(username='commenter', password='12345')
        response = str(client.get(reverse('pages:home')).content)
        self.assertTrue('<span class="font-weight-bold">Username:</span>commenter</p>' in response)
    
    def test_dashboard_in_blogger_nav_links(self):
        client = Client()
        client.login(username='scrubby', password='12345')
        response = str(client.get(reverse('pages:home')).content)
        self.assertTrue('<a href="/dashboard/">Dashboard</a>' in response)


