from django.db.models.signals import pre_save
from django.dispatch import receiver
import string, random
from django.utils.text import slugify
from .models import Product

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug = None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)
    
    Klass = instance.__class__
    max_length = Klass._meta.get_field('slug').max_length
    slug = slug[:max_length]
    qx_exists = Klass.objects.filter(slug = slug).exists()
    print(Klass)
    print(slug)
    print("----")

    if qx_exists:
        new_slug = "{slug}-{randstr}".format(
            slug = slug[:max_length-5], randstr = random_string_generator(size=5)
        )
        
        return unique_slug_generator(instance, new_slug = new_slug)
    
    return slug

@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)