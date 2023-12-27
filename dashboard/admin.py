from django.contrib import admin
from .models import Profile, Category, SubCategory, Product

# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)

