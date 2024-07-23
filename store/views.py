from django.shortcuts import render
from . import models

# Create your views here.

def get_categories():
    return models.Category.objects.all()

def index(request):
    featured_products = models.Product.objects.filter(is_featured=True).all()
    return render(request, 'index.html', {
        "featured_products":featured_products,
        "categories": get_categories()
    })

def shop(request):

    # Get query parameter from URL and filter products based on slug
    query_param = request.GET.get('q')
    if query_param:
        category = models.Category.objects.filter(slug = query_param).values('id')
        cate_id = category.get()['id']
        items = models.Product.objects.filter(category=cate_id).all()
        return render(request,'shop.html', {
        'items': items
        })
    
    items = models.Product.objects.all()
    return render(request,'shop.html', {
        'items': items,
        "categories": get_categories()
    })

def filter_shop(request, category):
    """filtering the products based on category"""
    category = models.Category.objects.filter(slug = category).values('id')
    cate_id = category.get()['id']
    items = models.Product.objects.filter(category=cate_id).all()
    return render(request,'shop.html', {
        'items': items,
        "categories": get_categories()
    })

def about(request):
    return render(request, 'about.html')

def checkout(request):
    return render(request, 'checkout.html')

def single_item(request, id, slug):
    single_item = models.Product.objects.filter(id=id).first()
    return render(request, 'shop-single.html', {
        "product": single_item,
        "categories": get_categories()
        })

def cart(request):
    return render(request, 'cart.html')

def contact(request):
    return render(request, 'contact.html')

def thank_you(request):
    return render(request, 'thankyou.html')
