from django.urls import path
from .consumers import CallConsumer

websocket_urlpatterns = [
    path(r"ws/call/$", CallConsumer.as_asgi()),
]
