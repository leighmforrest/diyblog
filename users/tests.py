from django.test import TestCase
from blog.tests.mixins import TestDataMixin

class UserTest(TestDataMixin, TestCase):
    def test_blogger_bio(self):
        blogger = self.blog1.blogger
        self.assertEqual(f'testuser is a blogger.', blogger.bio)
    
    def test_non_blogger_bio(self):
        user = self.commenter
        self.assertIsNone(user.bio)