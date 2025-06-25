from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.voice_response import VoiceResponse, Start

@csrf_exempt
def incoming_call(request):
    response = VoiceResponse()
    start = Start()
    start.stream(url='wss://prashant.jaxl.io/ws/call/')
    response.append(start)
    response.say("Hello, you're connected to the WebSocket.")
    return HttpResponse(str(response), content_type='text/xml')
