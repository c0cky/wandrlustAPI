import os
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.test.client import RequestFactory
from rest_framework import status
from faker import Factory
from v1.models import Post, Snippet, Video, Image
from v1.tests.base import BaseTest
from django.conf import settings


fake = Factory.create()


class TestPostsView(BaseTest):

    def test_should_successfully_create_a_post(self):
        """
        Ensure we can create a new post object.
        """
        url = '/api/v1/posts/'
        data = {
            'latitude': format(fake.latitude(), '.6f'),
            'longitude': format(fake.longitude(), '.6f'),
            'title': "here is a title"
        }
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.post(url, data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(response.data['latitude']), str(data['latitude']))
        self.assertEqual(str(response.data['longitude']),
                         str(data['longitude']))
        self.assertEqual(response.data['title'], data['title'])
        self.assertTrue(response.data['id'] is not None)

    def test_should_successfully_update_a_post(self):
        url = '/api/v1/posts/1/'
        data = {
            'title': 'do you even title bro?'
        }
        pre_put = Post.objects.get(pk=self.test_post.id)
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.put(url, data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_successfully_get_a_post(self):
        """
        Get a post and all of its attributes
        """
        url = '/api/v1/posts/1/'
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_successfully_update_a_post_image(self):
        url = '/api/v1/posts/1/images/1/'
        data = {
            'caption': fake.text()
        }
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.put(url, data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_post(self):
        """
        Try to get post that doesnt exist
        """
        url = '/api/v1/posts/123445234/'
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_successfully_create_an_image(self):
        """
        Ensure we can create an image
        """
        url = '/api/v1/posts/1/images/'
        image = SimpleUploadedFile(name='foo.gif',
                                   content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00'),
        data = {
            'image': image,
            'caption': fake.text()
        }
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.post(url, data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if settings.DEBUG:
            img = Image.objects.get(pk=2)
            os.remove(img.image.path)

    def test_should_un_successfully_create_an_image(self):
        """
        Ensure we can successfully stop bad images.
        """
        url = '/api/v1/posts/1/images/'
        data = {
            'image': 'bad-image-lol.jpg',
            'caption': fake.text()
        }
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.post(url, data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_sucessfully_get_a_post_images(self):
        """
        Ensure we can get a posts images
        """
        url = '/api/v1/posts/1/images/'
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_sucessfully_create_a_video(self):
        url = '/api/v1/posts/1/videos/'
        video = SimpleUploadedFile("file.mp4", "file_content",
                                   content_type="video/mp4")
        data = {
            'video': video,
            'caption': fake.text()
        }
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.post(url, data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if settings.DEBUG:
            vid = Video.objects.get(pk=2)
            os.remove(vid.video.path)

    def test_should_sucessfully_get_a_post_videos(self):
        url = '/api/v1/posts/1/videos/'
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_successfully_create_a_snippet(self):
        url = '/api/v1/posts/1/snippets/'
        data = {
            'snippet': fake.text(),
        }
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.post(url, data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_successfully_get_a_posts_snippets(self):
        url = '/api/v1/posts/1/snippets/'
        data = {
            'snippet': fake.text(),
        }
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.post(url, data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        with transaction.atomic():
            response = self.client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_successfully_get_a_post_with_all(self):
        url = '/api/v1/posts/1/'
        auth_headers = self.get_access_token_header()
        with transaction.atomic():
            response = self.client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_successfully_get_another_users_posts(self):
        url = '/api/v1/posts/user/'
        auth_headers = self.get_access_token_header()
        data = {
            'username': 'test_user'
        }
        with transaction.atomic():
            response = self.client.get(url, data=data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_should_successfully_get_a_comment(self):
    #     url = '/api/v1/posts/1/comments/'
    #     auth_headers = self.get_access_token_header()
    #     with transaction.atomic():
    #         response = self.client.get(url, **auth_headers)
    #     print response, url
