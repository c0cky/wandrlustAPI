from models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from v1.serializers import UserSerializer
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope


class UserViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [TokenHasReadWriteScope]
    pagination_class = PageNumberPagination
    safe_fields = ('id', 'username', 'url')

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

    @list_route(url_path='self')
    def self(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
