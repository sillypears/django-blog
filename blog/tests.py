from django.test import client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your tests here.

from .models import Post


class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@test.test',
            password='secretpasswordhehe',
        )

        self.post = Post.objects.create(
            title='Good one',
            body='Body content',
            author=self.user,
        )

    def test_string_representation(self):
        post = Post(title='A test title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'Good one')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Body content')

    def test_post_list_view(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Body content')
        self.assertTemplateUsed(resp, 'home.html')

    def test_post_detail_view(self):
        resp = self.client.get('/post/1')
        no_resp = self.client.get('/post/10000')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(no_resp.status_code, 404)
        self.assertContains(resp, 'Good one')
        self.assertTemplateUsed(resp, 'post_detail.html')
