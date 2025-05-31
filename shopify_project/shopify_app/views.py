# shopify_app/views.py
import shopify

from django.shortcuts import redirect, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from urllib.parse import urlencode

def shopify_login(request):
    print("------------------")
    shop = request.GET.get('shop')  # e.g. mystore.myshopify.com
    if not shop:
        return HttpResponse("Missing 'shop' parameter", status=400)

    shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)
    session = shopify.Session(shop,version = '2024-07')
    scopes = ["read_orders", "read_products"]
    permission_url = session.create_permission_url(scopes, settings.SHOPIFY_REDIRECT_URI)

    return redirect(permission_url)

# # shopify_app/views.py
# def shopify_callback(request):
#     shop_url = request.GET.get('shop')
#     if not shop_url:
#         print("***********")
#         return HttpResponse("Shop parameter missing", status=400)

#     session = shopify.Session(shop_url, version="2025-04")
#     token = session.request_token(request.GET)

#     # You can now store `shop_url` and `token` in your database
#     return HttpResponse(f"Shop connected: {shop_url}<br>Access Token: {token}")
from django.http import HttpResponseBadRequest

import hmac
import hashlib
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseRedirect

def validate_hmac(params, secret):
    hmac_from_shopify = params.pop("hmac", [None])[0]
    sorted_params = "&".join(
        f"{key}={','.join(value)}" for key, value in sorted(params.items())
    )
    computed_hmac = hmac.new(
        secret.encode("utf-8"),
        sorted_params.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(computed_hmac, hmac_from_shopify)
import hmac
import hashlib
from urllib.parse import urlencode

from django.http import HttpResponseBadRequest

def verify_hmac(request):
    params = request.GET.dict()
    received_hmac = params.pop('hmac', None)

    sorted_params = sorted((k, v) for k, v in params.items())
    message = urlencode(sorted_params)

    computed_hmac = hmac.new(
        key=bytes(os.getenv("SHOPIFY_API_SECRET"), 'utf-8'),
        msg=bytes(message, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(computed_hmac, received_hmac)
import requests
import os

def shopify_callback(request):
    if not verify_hmac(request):
        return HttpResponseBadRequest("HMAC verification failed")

    shop = request.GET.get("shop")
    code = request.GET.get("code")

    # Exchange temporary code for permanent access token
    token_url = f"https://{shop}/admin/oauth/access_token"
    data = {
        "client_id": os.getenv("SHOPIFY_API_KEY"),
        "client_secret": os.getenv("SHOPIFY_API_SECRET"),
        "code": code
    }
    response = requests.post(token_url, json=data)
    access_token = response.json().get("access_token")

    # Store this token securely for future use

    return redirect("/")  # or dashboard





def list_orders(request):
    token = request.session.get("access_token")
    shop = request.session.get("shop")

    if not token or not shop:
        return JsonResponse({"error": "Not authenticated"})

    shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)
    session = shopify.Session(shop, api_version="2025-04")
    session.token = token
    shopify.ShopifyResource.activate_session(session)

    orders = shopify.Order.find()
    order_data = [order.to_dict() for order in orders]

    return JsonResponse(order_data, safe=False)




from django.http import HttpResponse

def home(request):
    return HttpResponse("✅ Shopify app installed successfully. You can now fetch orders.")
