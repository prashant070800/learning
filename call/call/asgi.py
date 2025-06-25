"""
ASGI config for call project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from call_app.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack  # ✅ this is required

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "call.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(          # ✅ wrap with AuthMiddlewareStack
        URLRouter(
            websocket_urlpatterns
        )
    ),
})


