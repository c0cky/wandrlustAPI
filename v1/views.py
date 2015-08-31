from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
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
        serializer = self.get_serializer(self.queryset, many=True,
                                         fields=('id', 'username', 'url'))
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user, fields=('id',
                                                       'username', 'url'))
        return Response(serializer.data)

    @list_route(url_path='self')
    def self(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
