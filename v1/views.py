import hashlib
import random
from models import Post, User, Image, Video, Snippet, PostImage, PostSnippet, \
    PostVideo
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny
from v1.serializers import ImageSerializer, PostSerializer, UserSerializer, \
    SnippetSerializer, VideoSerializer, PostImageSerializer, \
    PostSnippetSerializer, PostVideoSerializer, CommentSerializer
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from oauth2_provider.models import AccessToken
from django_comments.models import Comment
from rest_framework.settings import api_settings


class UserViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    safe_fields = ('first_name', 'id', 'last_name', 'username', 'url')

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        # TODO: This needs to be more strict. POST && request
        # URL = /api/v1/users for instance. Same for activate.
        resolver = self.request.resolver_match
        view_name = resolver.view_name
        if self.request.method == 'POST':
            return (AllowAny(),)
        elif self.request.method == 'PUT' and view_name != 'user-self':
            return (AllowAny(),)
        else:
            return (TokenHasReadWriteScope(),)

    def list(self, request):
        users = User.objects.all()
        page = self.paginate_queryset(users)
        serializer = self.get_serializer(
            users, many=True, fields=self.safe_fields)

        if page is not None:
            serializer = self.get_serializer(
                page, many=True, fields=self.safe_fields)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user, fields=self.safe_fields)
        return Response(serializer.data)

    @list_route(methods=['put'], url_path='activate')
    def activate(self, request):
        try:
            user = User.objects.get(
                activation_token=request.data['activation_token']
                )
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if (request.data['activation_token'] == user.activation_token):
            user.is_active = True
            # change their token so they cant reactivate from email
            # after they try to delete
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            usernamesalt = user.username
            if isinstance(usernamesalt, unicode):
                usernamesalt = usernamesalt.encode('utf8')
            user.activation_token = hashlib.sha1(salt+usernamesalt).hexdigest()
            user.save()
        else:
            # Need to send some sort of error back.
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['put'], url_path='reset')
    def reset(self, request):
        user = User.objects.get(email=request.data['email'])
        try:
            password_token = request.data['password_token']
        except Exception:
            password_token = None
        if (password_token is None):
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            usernamesalt = user.username
            if isinstance(usernamesalt, unicode):
                usernamesalt = usernamesalt.encode('utf8')
            user.password_token = hashlib.sha1(salt+usernamesalt).hexdigest()
            message = "Hello, \n"
            message += "here is your token"
            message += user.password_token
            email = EmailMessage('Password Reset', message, to=[user.email])
            # email.send()
        else:
            if (request.data['password_token'] == user.password_token):
                user.set_password(request.data['password'])
                user.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['get', 'delete', 'put'], url_path='self')
    def self(self, request):
        if request.method == 'DELETE':
            user = User.objects.get(pk=request.user.id)
            if (user is not None):
                user.is_active = False
                user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            user = User.objects.get(id=request.user.id)
            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True,
                                             )
            if serializer.is_valid():
                serializer.save(owner=request.user)
                try:
                    user.set_password(request.data['password'])
                except Exception:
                    pass
                user.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        author = User.objects.get(id=request.user.id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        post.author = author
        post.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

    def list(self, request):
        queryset = Post.objects.filter()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            queryset, many=True)

        if page is not None:
            serializer = self.get_serializer(
                page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.filter()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    @list_route(methods=['get'], url_path='user')
    def user(self, request):
        username = request.query_params['username']
        user = User.objects.get(username=username)
        queryset = Post.objects.filter(author=user)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            queryset, many=True)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)


class ImageViewSet(viewsets.ModelViewSet):
    model = Image
    # parser_classes = (FileUploadParser,)
    queryset = PostImage.objects.all()
    serializer_class = ImageSerializer
    pagination_class = PageNumberPagination

    def create(self, request, post_pk=None):
        post = Post.objects.get(id=post_pk)
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.save()
        post_image = PostImage.objects.create(post=post, image=image,
                                              position=0)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, post_pk=None):
        queryset = PostImage.objects.filter(post=post_pk)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            queryset, many=True)

        if page is not None:
            serializer = self.get_serializer(
                page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, post_pk=None):
        queryset = PostImage.objects.filter(pk=pk, post=post_pk)
        image = get_object_or_404(queryset, pk=pk)
        serializer = PostImageSerializer(image)
        return Response(serializer.data)


class SnippetViewSet(viewsets.ModelViewSet):
    model = Snippet
    queryset = PostSnippet.objects.all()
    serializer_class = SnippetSerializer
    pagination_class = PageNumberPagination

    def create(self, request, post_pk=None):
        post = Post.objects.get(id=post_pk)
        serializer = SnippetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        snippet = serializer.save()
        post_snippet = PostSnippet.objects.create(post=post, snippet=snippet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, post_pk=None):
        queryset = Snippet.objects.filter(post=post_pk)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            queryset, many=True)

        if page is not None:
            serializer = self.get_serializer(
                page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, post_pk=None):
        queryset = PostSnippet.objects.filter(pk=pk, post=post_pk)
        snippet = get_object_or_404(queryset, pk=pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)


class VideoViewSet(viewsets.ModelViewSet):
    model = Video
    # parser_classes = (FileUploadParser,)
    queryset = PostVideo.objects.all()
    serializer_class = VideoSerializer
    pagination_class = PageNumberPagination

    def create(self, request, post_pk=None):
        post = Post.objects.get(id=post_pk)
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        video = serializer.save()
        post_video = PostVideo.objects.create(post=post, video=video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, post_pk=None):
        queryset = Video.objects.filter(post=post_pk)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            queryset, many=True)

        if page is not None:
            serializer = self.get_serializer(
                page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, post_pk=None):
        queryset = PostVideo.objects.filter(pk=pk, post=post_pk)
        video = get_object_or_404(queryset, pk=pk)
        serializer = VideotSerializer(video)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    model = Comment
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def create(self, request, post_pk=None):
        post = Post.objects.get(id=post_pk)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, post_pk=None):
        queryset = Comment.objects.filter(object_pk=post_pk)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            queryset, many=True)

        if page is not None:
            serializer = self.get_serializer(
                page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, post_pk=None):
        queryset = Comment.objects.filter(pk=pk, post=post_pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
