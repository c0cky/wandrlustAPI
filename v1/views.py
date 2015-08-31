from django.contrib.auth.models import User
from rest_framework import viewsets
from v1.serializers import UserSerializer
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [TokenHasReadWriteScope]
