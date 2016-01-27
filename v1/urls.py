from django.conf.urls import url, include
# from rest_framework import routers
from rest_framework_nested import routers
from v1 import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)

image_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
image_router.register(r'images', views.ImageViewSet, base_name='images')

video_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
video_router.register(r'videos', views.VideoViewSet, base_name='videos')

snippet_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
snippet_router.register(r'snippets', views.SnippetViewSet,
                        base_name='snippets')

# comment_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
# comment_router.register(r'comments', views.CommentViewSet,
#                         base_name='comments')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^v1/', include(image_router.urls)),
    url(r'^v1/', include(video_router.urls)),
    url(r'^v1/', include(snippet_router.urls))
    # url(r'^v1/', include(comment_router.urls))

]
