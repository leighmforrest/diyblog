from django.test import TestCase

from blog.forms import CommentForm


class TestCommentForm(TestCase):
    def test_valid_comment(self):
        data = {'content': 'Z'* 256}
        form = CommentForm(data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_comment(self):
        data = {'content': 'Z'* 1025}
        form = CommentForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'content': ['The comment is too long.']})
    
    def test_blank_comment(self):
        form = CommentForm({'content': ''})
        self.assertEqual(form.errors, {'content': ['This field is required.']})
    
    def test_comment_label(self):
        form = CommentForm()
        self.assertTrue(form.fields['content'].label == 'Description')