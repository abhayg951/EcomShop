from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
# Create your views here.

from .utils import get_categories, get_featured_products, get_brands, get_cart, get_cart_item_count

# home page
def index(request):
    return render(request, 'index.html', {
        "featured_products":get_featured_products(),
        "categories": get_categories(),
        "cart_data": get_cart(request)
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
        'breadcrumb_title': breadcrumb_title,
        "brand": get_brands(),
        "cart_data": get_cart(request)
    })

def filter_shop_by_category(request, category):
    """filtering the products based on category"""
    category = models.Category.objects.filter(slug = category).values('id')
    cate_id = category.get()['id']
    items = models.Product.objects.filter(category=cate_id).all()
    brand = models.Brands.objects.annotate(product_count=Count('product', filter=Q(product__category_id=cate_id))).order_by('-product_count')
    return render(request,'shop.html', {
        'items': items,
        "categories": get_categories(),
        "brand": brand,
        "cart_data": get_cart(request)
    })

def featured_products(request):
    breadcrumb_title = "Featured Shop"
    items = models.Product.objects.filter(is_featured=True)
    brand = models.Brands.objects.annotate(product_count=Count('product', filter=Q(product__is_featured=True))).order_by('-product_count')
    return render(request, 'shop.html', {
        'items': items,
        'categories': get_categories(),
        'breadcrumb_title': breadcrumb_title,
        "brand": brand,
        "cart_data": get_cart(request)
    })

def filter_by_collection(request, collection):
    """Filtering the products based on collection"""
    breadcrumb_title = f"{collection} Store"
    items = models.Product.objects.filter(collection=collection)
    return render(request, 'shop.html', {
        'items': items,
        'categories': get_categories(),
        'breadcrumb_title': breadcrumb_title,
        "brand": get_brands(),
        "cart_data": get_cart(request)
    })


def single_item(request, id, slug):
    decoded_id = models.Product.decode_id(id)
    single_item = models.Product.objects.filter(id=decoded_id, slug=slug).first()
    item_images = models.ProductImage.objects.filter(product=single_item).all()
    return render(request, 'shop-single.html', {
        "product": single_item,
        "categories": get_categories(),
        "featured_products":get_featured_products(),
        "item_images": item_images,
        "cart_data": get_cart(request)
        })

# cart related functions


def add_to_cart(request):
    """this function adds the products to the carts"""
    product_id = request.GET['id']
    product = get_object_or_404(models.Product, id=product_id)
    encoded_id = product.encoded_id()
    # if user is logged in,(cart will added to the database)
    if request.user.is_authenticated:

        """adding data to the database"""
        cart, created = models.Cart.objects.get_or_create(user=request.user)
        cart_item, created = models.CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        '''adding data to the session to update the cart'''
        cart_product = {}
        
        cart_product[str(product_id)] = {
            'title': request.GET['title'],
            'price': request.GET['price'],
            'quantity': int(request.GET['qty']),
            'total': float(request.GET['price']) * int(request.GET['qty']),
            'image': request.GET['img']
        }

        cart_count = get_cart_item_count(request)
        print(get_cart_item_count(request))

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
        
        if 'cart_count' in request.session:
            request.session['cart_count'] = cart_count
        else:
            request.session['cart_count'] = cart_count
        
        print("Cart data: ", request.session['cart_count'])
        return JsonResponse({"data":request.session['cart_data_obj'], 'total_cart_items': cart_count})
    
    # For Guest Users
    # if user is not logged in, then cart will only added to the session
    else:
        cart_product = {}
        product_id = request.GET['id']
        cart_product[str(product_id)] = {
            'id': encoded_id,
            'slug': request.GET['slug'],
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
    
        # print("Cart data: ", request.session['cart_count'])
        return JsonResponse({"data":request.session['cart_data_obj'], 'total_cart_items': len(request.session['cart_data_obj'])})

def cart_view(request):
    """Display the cart page"""
    print("this function is called")

    """if user is logged in"""
    if request.user.is_authenticated:
        cart, created = models.Cart.objects.get_or_create(user=request.user)
        cart_item = models.CartItem.objects.filter(cart=cart)
        total_price = sum(item.total_price() for item in cart_item)
        context = {
            'cart_data': cart_item,
            'total_cart_items': cart_item.count(),
            'total_price': total_price,
            'categories': get_categories(),
        }

        print(context)
        return render(request, 'cart.html', context)
    
    else:
        if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}
            

        return render(request, 'cart.html', {
            'cart_data': request.session['cart_data_obj'],
            'total_cart_items': len(request.session['cart_data_obj']),
            'categories': get_categories(),
        })


def about(request):
    return render(request, 'about.html')

@login_required
def checkout(request):

    # redirect back to cart when cart is empty


    # print(request.session.items())

    # for logged in user 
    if request.user.is_authenticated:
        cart, created = models.Cart.objects.get_or_create(user=request.user)
        cart_item = models.CartItem.objects.filter(cart=cart)
        total_price = sum(item.total_price() for item in cart_item)
        context = {
            'cart_data': cart_item,
            'total_cart_items': cart_item.count(),
            'total_price': total_price,
            'categories': get_categories(),
        }

        print(context)
        return render(request, 'checkout.html', context)
    
    if 'cart_data_obj' not in request.session:
        request.session['cart_data_obj'] = {}
        return redirect('store:cart')
    elif request.session['cart_data_obj'] == {}:
        return redirect('store:cart')

    return render(request, 'checkout.html', {
        'cart_data': request.session['cart_data_obj'],
        'total_cart_items': len(request.session['cart_data_obj']),
        'categories': get_categories(),
    })


def contact(request):
    return render(request, 'contact.html')

def thank_you(request):
    return render(request, 'thankyou.html')
