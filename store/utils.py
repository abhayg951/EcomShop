from . import models
from django.db.models import Count

def get_categories():
    return models.Category.objects.all()

def get_featured_products():
    return models.Product.objects.filter(is_featured=True).all()

def get_brands():
    return models.Brands.objects.annotate(product_count=Count('product')).order_by('-product_count')

def get_cart(request):
    cart_item = {}
    if request.user.is_authenticated:
        cart, created = models.Cart.objects.get_or_create(user=request.user)
        cart_item = models.CartItem.objects.filter(cart=cart)
    return cart_item

def get_cart_item_count(request):
    '''this will count the number of items in the cart of login user'''
    user = request.user
    if user.is_authenticated:
        cart, created = models.Cart.objects.get_or_create(user=user)
        cart_item = models.CartItem.objects.filter(cart=cart)
        return cart_item.count()