from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

#create Serializer type model serializer
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=64,
        min_length=8,
        write_only=True
    )

    #setToken to be readonly
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        #set field that can include in req.
        fields = ['email', 'name', 'password', 'token']

    def create(self, validated_data):
        #**mean arbitrary number of keyword arguments as input.
        return User.objects.create_user(**validated_data)


#create Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        #custom validate function
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'name': user.name,
            'token': user.token
        }