# shopify_app/views.py
import shopify

from django.shortcuts import redirect, HttpResponse
from django.http import JsonResponse
from django.conf import settings

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
import shopify

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

def shopify_callback(request):
    shopify.Session.setup(
        api_key=settings.SHOPIFY_API_KEY,
        secret=settings.SHOPIFY_API_SECRET,
    )

    shop_url = request.GET.get("shop")
    if not shop_url:
        return HttpResponseBadRequest("Missing shop parameter")

    # Copy QueryDict to a mutable dict
    params = request.GET.copy()

    if not validate_hmac(params, settings.SHOPIFY_API_SECRET):
        return HttpResponseBadRequest("❌ Invalid HMAC: Possibly malicious login")

    session = shopify.Session(shop_url, version="2025-04")
    token = session.request_token(request.GET.dict())

    request.session["access_token"] = token
    request.session["shop"] = shop_url

    return HttpResponseRedirect("/shopify/orders/")



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
