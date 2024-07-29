from django.db import models
import uuid
import PIL.Image
from django.urls import reverse
from django.utils.html import format_html
import base64

from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

COLLECTION_CHOICE = (
    ('Children', 'Children'),
    ('Women', 'Women'),
    ('Men', 'Men'),
)

class Brands(models.Model):
    name = models.CharField(max_length=100, verbose_name="Brand Name")
    slug = models.SlugField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self) -> str:
        return f"{self.name}"

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid1, primary_key=True, editable=False)
    name = models.CharField(null=False, max_length=100, blank=False)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    image = models.ImageField(upload_to="categories", null=True, verbose_name="Category Image")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f"{self.name}"

    def get_category_image(self):
        return format_html("<img src='%s' alt='Category Image' width='50' height='50'/>" % (self.image.url))

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(null=False, max_length=255, blank=False)
    brand = models.ForeignKey(Brands, verbose_name ="Brand Name", on_delete=models.CASCADE)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    stock = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    is_featured = models.BooleanField(default=False)
    collection = models.CharField(choices=COLLECTION_CHOICE, max_length=10, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('-created_at', )
        verbose_name_plural = "Products"
    
    def __str__(self)  -> str:
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = PIL.Image.open(self.image)
        # width, height = img.size
        target_width = 480
        target_height = 340
        img = img.resize((int(target_width), int(target_height)), PIL.Image.LANCZOS)
        img.save(self.image.path, quality=100)
        img.close()
        self.image.close()

    
    def product_image(self) -> str:
        # return html_safe("<img src='%s', width='50' height='50'/>" % (self.image.url))
        return format_html(f'<img src="{self.image.url}" width="50" height="50">')
    
    def encoded_id(self) -> str:
        encoded_bytes = base64.urlsafe_b64encode(self.id.bytes)
        return encoded_bytes.decode('utf-8').rstrip('=')

    @staticmethod
    def decode_id(encoded_id: str) -> uuid.UUID:
        # Add padding if necessary
        padded_encoded_id = encoded_id + '=' * (-len(encoded_id) % 4)
        decoded_bytes = base64.urlsafe_b64decode(padded_encoded_id)
        return uuid.UUID(bytes=decoded_bytes)

class ProductImage(models.Model):
    images = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='images', null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

class Cart(models.Model):
    pass

