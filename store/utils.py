from . import models

def get_categories():
    return models.Category.objects.all()

def get_featured_products():
    return models.Product.objects.filter(is_featured=True).all()