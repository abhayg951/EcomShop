from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.index, name="home"),
    path("about", views.about, name="about"),
    path("cart", views.cart, name="cart"),
    path("store/", views.shop, name="store"),
    path("store/<slug:slug>/<str:id>", views.single_item, name="single_item"),
    path("store/<str:category>", views.filter_shop, name="filter_shop"),
    path("contact", views.contact, name="contact"),
    path("cart", views.cart, name="cart"),
    path("thank-you", views.thank_you, name="thank_you"),
]
