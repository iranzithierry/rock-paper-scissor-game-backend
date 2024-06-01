from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.filters import SearchFilter, OrderingFilter


from src.users.models import User
from src.users.permissions import IsUserOrReadOnly
from src.users.serializers import (
    CreateUserSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
)


class UserViewSet(
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin,
    mixins.UpdateModelMixin, 
    viewsets.GenericViewSet, 
):
    """
    Creates, Updates and Retrieves - User Accounts
    """

    queryset = User.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["email", "username"]
    ordering_fields = ["username"]
    serializers = {'default': UserSerializer, 'create': CreateUserSerializer}
    permissions = {'default': (IsUserOrReadOnly,), 'create': (AllowAny,)}

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def get_user_data(self, instance):
        try:
            return Response(UserSerializer(self.request.user, context={'request': self.request}).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Wrong auth token' + e}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
