import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.local")

# Ensure the settings are configured and the application is ready before importing other modules
django_asgi_app = get_asgi_application()

# from config import routing
from app import routing
from app.base.middleware import JwtAuthMiddlewareStack

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            JwtAuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
        ),
    }
)
