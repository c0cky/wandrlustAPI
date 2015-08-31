from django.conf.urls import url, include
from rest_framework import routers
from v1 import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^v1/', include(router.urls)),
]
