import hashlib
import random
from models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
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

    @list_route(methods=['post'], url_path='activate')
    def activate(self, request):
        print request.data
        user = User.objects.get(username=request.data['username'])
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
            return Response()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @list_route(methods=['post'], url_path='reset')
    def reset(self, request):
        user = User.objects.get(username=request.data['username'])
        if (request.data['password_token'] is None):
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            usernamesalt = user.username
            if isinstance(usernamesalt, unicode):
                usernamesalt = usernamesalt.encode('utf8')
            user.password_token = hashlib.sha1(salt+usernamesalt).hexdigest()
        else:
            if (request.data['password_token'] == user.password_token):
                user.set_password(request.password)
                user.save()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @list_route(url_path='self')
    def self(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @list_route(url_path='delete')
    def destroy(self, request, pk=None):
        user = User.objects.get(username=request.data['username'])
        if (user is not None):
            user.is_active = False
            user.save()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
