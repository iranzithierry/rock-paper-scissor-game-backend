import os
import sys
from pathlib import Path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "src"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings.local")

# Ensure the settings are configured and the application is ready before importing other modules
django_asgi_app = get_asgi_application()

from src import routing  # Import routing after initializing Django ASGI app
from src.games.asgi.middleware import JwtAuthMiddlewareStack  # Import middleware after initializing Django ASGI app

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            JwtAuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
        ),
    }
)
