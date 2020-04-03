from rest_framework import serializers

from .models import User


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