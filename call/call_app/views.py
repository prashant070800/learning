from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from django.conf import settings

@csrf_exempt
def make_call(request):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    call = client.calls.create(
        twiml=f'<Response><Start><Stream url="wss://prashant.jaxl.io/ws/call/"/></Start><Say>Connecting to WebSocket</Say></Response>',
        to=request.GET.get('to'),
        from_=settings.TWILIO_PHONE_NUMBER,
    )
    return JsonResponse({"sid": call.sid})
