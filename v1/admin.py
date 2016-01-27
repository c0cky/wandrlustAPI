from django.contrib import admin
from models import User, Snippet, Image, Video, Post, PostImage, PostVideo, \
                    PostSnippet

admin.site.register(User)
admin.site.register(Snippet)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostVideo)
admin.site.register(PostSnippet)
