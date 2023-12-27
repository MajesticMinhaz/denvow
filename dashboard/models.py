from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=150)

    profile_pic = ProcessedImageField(
        upload_to='avater', 
        blank=True, 
        null=True, 
        default='avater/default/avater.png',
        processors=[ResizeToFill(600, 600)],
        format='JPEG',
        options={
            'quality': 90
        },

    )

    about = models.TextField(blank=True, null=True, default=None, max_length=250)
    facebook = models.URLField(blank=True, null=True, default=None)
    instagram = models.URLField(blank=True, null=True, default=None)
    twitter = models.URLField(blank=True, null=True, default=None)
    linkedin = models.URLField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username} Profile'
    

class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)

    image = ProcessedImageField(
        upload_to='categories',
        processors=[ResizeToFill(600, 600)],
        format='JPEG',
        options={
            'quality': 90
        },

    )

    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    

class SubCategory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    image = ProcessedImageField(
        upload_to='sub-categories',
        processors=[ResizeToFill(600, 600)],
        format='JPEG',
        options={
            'quality': 90
        },
    )

    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=150)
    image = ProcessedImageField(
        upload_to='products',
        processors=[ResizeToFill(600, 600)],
        format='JPEG',
        options={
            'quality': 90
        },
    )

    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    sub_category = models.ForeignKey(
        SubCategory, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    pass


class Suplier(models.Model):
    pass
