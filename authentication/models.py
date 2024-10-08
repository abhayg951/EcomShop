from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.urls import reverse
import uuid

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')), null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.PositiveBigIntegerField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', "first_name", "last_name"]


    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})

    def user_picture(self):
        if self.profile_picture:
            return format_html("<img src='%s' alt='Client Image' width='50' height='50'/>" % (self.profile_picture.url))
        else:
            return ''