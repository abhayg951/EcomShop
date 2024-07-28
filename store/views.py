from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import models
from django.db.models import Q
# from django.core.paginator import Paginator

# Create your views here.

from .utils import get_categories, get_featured_products

# home page
def index(request):
    return render(request, 'index.html', {
        "featured_products":get_featured_products(),
        "categories": get_categories()
    })

# store functions
def shop(request):
    query_param = request.GET.get('q')
    # page_number = request.GET.get('page')
    breadcrumb_title = "Shop"
    if query_param:
        # Search for featured products if query is 'featured'
        if query_param == "featured":
            breadcrumb_title = "Featured Shop"
            items = models.Product.objects.filter(is_featured=True)
        else:
            # Try to find the category by slug
            category = models.Category.objects.filter(slug=query_param).first()
            if category:
                # Filter products by category
                items = models.Product.objects.filter(category=category)
            else:
                # Search for products by name or description
                items = models.Product.objects.filter(
                    Q(name__icontains=query_param) |
                    Q(description__icontains=query_param) |
                    Q(brand__icontains=query_param)
                )
    
    else:
        # If no query parameter is provided, return all products
        items = models.Product.objects.all()
    
    # Pagination
    # paginator = Paginator(items, 20)  # Show 20 items per page
    # page_obj = paginator.get_page(page_number)

    
    return render(request, 'shop.html', {
        'items': items,
        'categories': get_categories(),
        'breadcrumb_title': breadcrumb_title
    })

def filter_shop_by_category(request, category):
    """filtering the products based on category"""
    category = models.Category.objects.filter(slug = category).values('id')
    cate_id = category.get()['id']
    items = models.Product.objects.filter(category=cate_id).all()
    return render(request,'shop.html', {
        'items': items,
        "categories": get_categories()
    })

def featured_products(request):
    breadcrumb_title = "Featured Shop"
    items = models.Product.objects.filter(is_featured=True)
    return render(request, 'shop.html', {
        'items': items,
        'categories': get_categories(),
        'breadcrumb_title': breadcrumb_title
    })


def single_item(request, id, slug):
    decoded_id = models.Product.decode_id(id)
    single_item = models.Product.objects.filter(id=decoded_id, slug=slug).first()
    return render(request, 'shop-single.html', {
        "product": single_item,
        "categories": get_categories(),
        "featured_products":get_featured_products()
        })

# cart related functions

def add_to_cart(request):
    """this function adds the products to the carts"""
    cart_product = {}
    product_id = request.GET['id']
    cart_product[str(product_id)] = {
        'title': request.GET['title'],
        'price': request.GET['price'],
        'quantity': int(request.GET['qty']),
        'total': float(request.GET['price']) * int(request.GET['qty']),
        'image': request.GET['img']
    }

    if 'cart_data_obj' in request.session:
        if str(product_id) in request.session['cart_data_obj']:
            cart_data = request.session["cart_data_obj"]
            cart_data[str(product_id)]['quantity'] = int(cart_product[str(product_id)]["quantity"])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session["cart_data_obj"]
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    
    print("Cart data: ", request.session['cart_data_obj'])
    return JsonResponse({"data":request.session['cart_data_obj'], 'total_cart_items': len(request.session['cart_data_obj'])})


def cart(request):
    """Display the cart page"""
    print("this function is called")
    if 'cart_data_obj' not in request.session:
        request.session['cart_data_obj'] = {}


    return render(request, 'cart.html', {
        'cart_data': request.session['cart_data_obj'],
        'total_cart_items': len(request.session['cart_data_obj']),
        'categories': get_categories(),
    })
    return render(request, 'cart.html')


def about(request):
    return render(request, 'about.html')

def checkout(request):
    return render(request, 'checkout.html')


def contact(request):
    return render(request, 'contact.html')

def thank_you(request):
    return render(request, 'thankyou.html')
