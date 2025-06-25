from django.urls import path
from .views import make_call
from .twilio_views import incoming_call

urlpatterns = [
    path("api/call/", make_call),
    path("twilio/incoming/", incoming_call),
]
