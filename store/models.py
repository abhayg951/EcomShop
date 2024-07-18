from django.db import models
import uuid
import PIL.Image

# Create your models here.

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid1, primary_key=True, editable=False)
    name = models.CharField(null=False, max_length=100, blank=False)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

    def __str__(self) -> str:
        return f"{self.slug}"

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(null=False, max_length=255, blank=False)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    stock = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

    class Meta:
        ordering = ('-created_at', )
    
    def __str__(self)  -> str:
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = PIL.Image.open(self.image)
        # width, height = img.size
        target_width = 253
        target_height = 180
        img = img.resize((int(target_width), int(target_height)), PIL.Image.LANCZOS)
        img.save(self.image.path, quality=100)
        img.close()
        self.image.close()

