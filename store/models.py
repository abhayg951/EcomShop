from django.db import models
import uuid

# Create your models here.

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(null=False, max_length=255, blank=False)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    stock = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.name