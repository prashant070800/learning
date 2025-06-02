# shopify_app/views.py

import shopify
import hmac
import hashlib

from django.conf import settings
from django.shortcuts import redirect
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)


# Shopify Login View
def shopify_login(request):
    shop = request.GET.get('shop')  # e.g., mystore.myshopify.com
    if not shop:
        return HttpResponse("Missing 'shop' parameter", status=400)

    # Setup Shopify session
    shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)
    
    # Create session with consistent version
    session = shopify.Session(shop, version='2024-07')  # Match version to your app configuration
    scopes = ["read_orders", "read_products"]
    permission_url = session.create_permission_url(scopes, settings.SHOPIFY_REDIRECT_URI)

    return redirect(permission_url)


# Shopify HMAC Validation
def validate_hmac(params, secret):
    """Validate the HMAC to ensure authenticity of the request"""
    hmac_from_shopify = params.pop("hmac", None)
    if isinstance(hmac_from_shopify, list):
        hmac_from_shopify = hmac_from_shopify[0]

    sorted_params = "&".join(
        f"{key}={value}" for key, value in sorted(params.items())
    )

    computed_hmac = hmac.new(
        secret.encode("utf-8"),
        sorted_params.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(computed_hmac, hmac_from_shopify)


# Shopify Callback View
def shopify_callback(request):
    shop_url = request.GET.get("shop")
    if not shop_url:
        return HttpResponseBadRequest("Missing 'shop' parameter")

    shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)
    params = request.GET.copy()

    if not validate_hmac(params, settings.SHOPIFY_API_SECRET):
        return HttpResponseBadRequest("❌ Invalid HMAC: Possibly malicious login")

    session = shopify.Session(shop_url, version="2024-07")
    token = session.request_token(request.GET.dict())

    # ✅ Print the token
    print(f"\n🔑 ACCESS TOKEN for {shop_url}:\n{token}\n")

    # Optionally store token for later use
    request.session["access_token"] = token
    request.session["shop"] = shop_url

    return HttpResponseRedirect("/shopify/orders/")


# Fetch Orders View
def list_orders(request):
    token = request.session.get("access_token")
    shop = request.session.get("shop")

    if not token or not shop:
        return JsonResponse({"error": "Not authenticated"}, status=403)

    # Setup and activate session with access token
    shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)
    session = shopify.Session(shop, version="2024-07")
    session.token = token
    shopify.ShopifyResource.activate_session(session)

    try:
        orders = shopify.Order.find()
        order_data = [order.to_dict() for order in orders]
        return JsonResponse(order_data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        shopify.ShopifyResource.clear_session()


# Optional: Simple Home View
def home(request):
    return HttpResponse("✅ Shopify app installed successfully. You can now fetch orders.")
