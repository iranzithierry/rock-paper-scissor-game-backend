"""General web socket middlewares
"""

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from jwt.exceptions import InvalidSignatureError, InvalidKeyError, InvalidTokenError
from django.conf import settings
from app.users.models import User
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(validated_token):
    try:
        user = User.objects.get(id=validated_token["user_id"])
        return user
    except User.DoesNotExist:
        return None



class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
       # Close old database connections to prevent usage of timed out connections
        close_old_connections()
        # Get the token
        token = parse_qs(scope["query_string"].decode("utf8")).get("token", None)
        if token:
            token = token[0]
        else:
            return None
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            return None
        else:
            try:
                decoded_data = jwt_decode(token, settings.APP_JWT_SIGNING_KEY, algorithms=["HS256"])
            except (InvalidSignatureError, InvalidKeyError, InvalidTokenError) as e:
                return None
            
            user = await get_user(validated_token=decoded_data)
            if not user:
                return None
            
            scope["user"] = user
        try:
           return await super().__call__(scope, receive, send)
        except ValueError as e:
            return None


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))