import base64
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from rest_framework.test import APITestCase
from oauth2_provider.models import AccessToken, get_application_model
from oauth2_provider.settings import oauth2_settings
from v1.models import Post, User, Image, Video, Snippet, PostSnippet, \
    PostImage, PostVideo
from datetime import timedelta
from django.conf import settings
from django.test import override_settings

Application = get_application_model()


@override_settings(DEBUG=True)
class BaseTest(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            username="test_user",
            email="test@user.com",
            first_name="Trevor",
            last_name="Hutto",
            password="123456",
            bio="this is me.",
            profile_picture=SimpleUploadedFile(name='foo.gif',
                                     content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00'),
            header_picture=SimpleUploadedFile(name='foo.gif',
                                     content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00'),

        )

        self.dev_user = User.objects.create_user(
            username="dev_user",
            email="dev@user.com",
            first_name="Camron",
            last_name="Godbout",
            password="123456"
        )

        self.test_post = Post.objects.create(
            author=self.test_user,
            title="title",
            latitude="1.123123",
            longitude="1.123123"
        )

        self.test_image = Image.objects.create(
            image=SimpleUploadedFile(name='foo.gif',
                                     content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00'),
            caption="here es captiones"
        )

        self.test_video = Video.objects.create(
            video=SimpleUploadedFile("file.mp4", "file_content",
                                     content_type="video/mp4"),
            caption="here es captiones"
        )

        self.test_snippet = Snippet.objects.create(
            snippet="here is a snippet"
        )

        self.post_snippet = PostSnippet.objects.create(
            snippet=self.test_snippet,
            post=self.test_post,
            position=0
        )
        self.post_video = PostVideo.objects.create(
            video=self.test_video,
            post=self.test_post
        )

        self.post_image = PostImage.objects.create(
            image=self.test_image,
            post=self.test_post,
            position=1
        )

        self.application = Application(
            name="Test Application",
            redirect_uris="http://example.com",
            user=self.dev_user,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()

        self.access_token = AccessToken(
            user=self.test_user,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=300),
            token='secret-access-token-key',
            application=self.application
        )
        self.access_token.save()

        oauth2_settings._SCOPES = ['read', 'write']

    def tearDown(self):
        self.application.delete()
        self.test_user.delete()
        if settings.DEBUG:
            if self.test_user.profile_picture:
                if os.path.isfile(self.test_user.profile_picture.path):
                    os.remove(self.test_user.profile_picture.path)
            if self.test_user.header_picture:
                if os.path.isfile(self.test_user.header_picture.path):
                    os.remove(self.test_user.header_picture.path)
        self.dev_user.delete()
        if settings.DEBUG:
            if self.test_image.image:
                if os.path.isfile(self.test_image.image.path):
                    os.remove(self.test_image.image.path)
        self.test_image.delete()
        self.test_post.delete()
        self.test_snippet.delete()
        if settings.DEBUG:
            if self.test_video.video:
                if os.path.isfile(self.test_video.video.path):
                    os.remove(self.test_video.video.path)
        self.test_video.delete()

    def get_basic_auth_header(self, user, password):
        """
        Return a dict containg the correct headers to set to make
        HTTP Basic Auth request
        """
        user_pass = '{0}:{1}'.format(user, password)
        auth_string = base64.b64encode(user_pass.encode('utf-8'))
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + auth_string.decode("utf-8"),
        }

        return auth_headers

    def get_access_token_header(self):
        """
        Return a dict containing the correct headers to set to make
        an authorized request.
        """
        access_token_header = {
            'Authorization': 'Bearer ' + self.access_token.token
        }

        return access_token_header
