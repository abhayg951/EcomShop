from django.shortcuts import render
from . import models
from django.db.models import Q
# from django.core.paginator import Paginator

# Create your views here.

def get_categories():
    return models.Category.objects.all()

def get_featured_products():
    return models.Product.objects.filter(is_featured=True).all()

def index(request):
    return render(request, 'index.html', {
        "featured_products":get_featured_products(),
        "categories": get_categories()
    })

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
    print("this is the decoded id", decoded_id)
    single_item = models.Product.objects.filter(id=decoded_id, slug=slug).first()
    return render(request, 'shop-single.html', {
        "product": single_item,
        "categories": get_categories(),
        "featured_products":get_featured_products()
        })

def about(request):
    return render(request, 'about.html')

def checkout(request):
    return render(request, 'checkout.html')

def cart(request):
    return render(request, 'cart.html')

def contact(request):
    return render(request, 'contact.html')

def thank_you(request):
    return render(request, 'thankyou.html')
