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

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1')

    def test_post_create_view(self):
        resp = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New text',
            'author': self.user,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'New title')
        self.assertContains(resp, 'New text')

    def test_post_update_view(self):  # new
        resp = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated title',
            'body': 'Updated text',
        })
        self.assertEqual(resp.status_code, 302)

    def test_post_delete_view(self):  # new
        response = self.client.get(
            reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)
