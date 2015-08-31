from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from v1.serializers import UserSerializer
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [TokenHasReadWriteScope]

    def list(self, request):
    	queryset = User.objects.all()
    	serializer = self.get_serializer(queryset, many=True, fields=('id', 'username', 'url'))
    	return Response(serializer.data)

    @list_route(url_path='self')
    def self(self, request):
    	serializer = self.get_serializer(request.user)
    	return Response(serializer.data)