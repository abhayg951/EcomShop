from django.contrib import admin
from . import models

# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = models.ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ["name", "product_image", "price"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "get_category_image"]

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
# admin.site.register(models.)