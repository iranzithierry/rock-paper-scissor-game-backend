from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from src.users.models import User
from rest_framework import exceptions
from rest_framework_simplejwt.state import token_backend
from src.common.serializers import ThumbnailerJSONSerializer


class UserSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailerJSONSerializer(required=False, allow_null=True, alias_target='src.users')

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'profile_picture',
        )
        read_only_fields = ('username',)


class CreateUserSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailerJSONSerializer(required=False, allow_null=True, alias_target='src.users')
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, user):
        return user.get_tokens()

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id','username','email','password','profile_picture','tokens',)
        read_only_fields = ('tokens',)
        extra_kwargs = {'password': {'write_only': True}}
    

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        tokens = data.copy()
        user = UserSerializer(self.user).data
        user['tokens'] = tokens
 
        return user

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Inherit from `TokenRefreshSerializer` and touch the database
    before re-issuing a new access token and ensure that the user
    exists and is active.
    """
    error_msg = 'No active account found with the given credentials'

    def validate(self, attrs):
        token_payload = token_backend.decode(attrs['refresh'])
        try:
            User.objects.get(pk=token_payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )

        return super().validate(attrs) 

class PlayerSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailerJSONSerializer(required=False, allow_null=True, alias_target='src.users')

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'profile_picture',
        )
