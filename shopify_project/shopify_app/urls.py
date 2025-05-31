# shopify_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),  # 🔥 this handles the "/" route
    path('shopify/login/', views.shopify_login),
    path('shopify/callback/', views.shopify_callback),
    path("shopify/orders/", views.list_orders),

]
