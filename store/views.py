from django.shortcuts import render
from . import models

# Create your views here.

def index(request):
    return render(request, 'index.html')

def shop(request):
    items = models.Product.objects.all()
    return render(request,'shop.html', {
        'items': items
    })

def about(request):
    return render(request, 'about.html')

def checkout(request):
    return render(request, 'checkout.html')

def single_item(request, id, slug):
    single_item = models.Product.objects.filter(id=id).first()
    return render(request, 'shop-single.html')

def cart(request):
    return render(request, 'cart.html')

def contact(request):
    return render(request, 'contact.html')

def thank_you(request):
    return render(request, 'thankyou.html')
