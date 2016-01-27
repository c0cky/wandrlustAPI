# from django.core.mail import EmailMessage
from models import Image, Post, Snippet, User, Video, PostImage, PostSnippet, \
    PostVideo
from rest_framework import serializers
from django_comments.models import Comment


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username',
                  'password', 'bio', 'header_picture', 'profile_picture')
        # so the password isnt returned after POST
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CommentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Comment


class VideoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'video', 'caption')


class ImageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Image
        # fields = ('image_file', 'caption')


class SnippetSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'snippet')


class PostVideoSerializer(DynamicFieldsModelSerializer):
    video = VideoSerializer(read_only=True)

    class Meta:
        model = PostVideo
        fields = ('id', 'video', 'position')


class PostImageSerializer(DynamicFieldsModelSerializer):
    image = ImageSerializer(read_only=True)

    class Meta:
        model = PostImage
        fields = ('id', 'image', 'position')


class PostSnippetSerializer(DynamicFieldsModelSerializer):
    snippet = SnippetSerializer(read_only=True)

    class Meta:
        model = PostSnippet
        fields = ('id', 'snippet', 'position')


class PostSerializer(DynamicFieldsModelSerializer):
    images = PostImageSerializer(many=True,
                                 read_only=True,
                                 source='get_images')
    snippets = PostSnippetSerializer(many=True,
                                     read_only=True,
                                     source='get_snippets')
    videos = PostVideoSerializer(many=True,
                                 read_only=True,
                                 source='get_videos')

    comments = CommentSerializer(many=True,
                                 read_only=True,
                                 source='get_comments')

    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'submitted_date', 'latitude',
                  'longitude', 'title', 'images', 'videos', 'snippets',
                  'comments')
        depth = 4

    def create(self, validated_attrs):
        post = Post.objects.create(**validated_attrs)
        post.save()
        return post
