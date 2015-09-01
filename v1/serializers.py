import hashlib
import random
# from django.core.mail import EmailMessage
from models import User
from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.HyperlinkedModelSerializer):
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
        fields = ('id', 'email', 'username', 'password', 'groups', 'url')
        # so the password isnt returned after POST
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = validated_data['username']
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            activation_token=hashlib.sha1(salt+usernamesalt).hexdigest(),
        )
        user.is_active = False
        user.save()
        # message = "Enter email message here"
        # email = EmailMessage('Activate', message, to=validated_data['email'])
        # email.send()

        return user
