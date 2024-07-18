from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about", views.about, name="about"),
    path("cart", views.cart, name="cart"),
    path("shop", views.shop, name="shop"),
    path("shop/<slug:slug>/<str:id>", views.single_item, name="single-item"),
    path("contact", views.contact, name="contact"),
    path("cart", views.cart, name="cart")
]
