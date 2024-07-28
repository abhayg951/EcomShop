from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    # home page
    path("", views.index, name="home"),
    # about page
    path("about", views.about, name="about"),
    
    # main store page
    path("store/", views.shop, name="store"),
    path("store/featured", views.featured_products, name="featured_products"),
    path("store/<str:id>/<slug:slug>", views.single_item, name="single-item"),
    path("store/<str:category>", views.filter_shop_by_category, name="filter_shop"),

    # contact us
    path("contact", views.contact, name="contact"),
    
    # cart 
    path("cart", views.cart, name="cart"),
    path("add-to-cart", views.add_to_cart, name="add-to-cart"),
    
    # checkout
    path("checkout", views.checkout, name="checkout"),
    
    # Thank you page
    path("thank-you", views.thank_you, name="thank_you"),
]
