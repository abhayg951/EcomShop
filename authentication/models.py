from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.urls import reverse
import uuid

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')), null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.PositiveBigIntegerField(null=True, blank=True)

    username = None


    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})

    def get_profile_picture_url(self):
        if self.profile_picture:
            return format_html("<img src='%s' alt='Client Image' width='50' height='50'/>" % (self.profile_picture.url))
        else:
            return ''