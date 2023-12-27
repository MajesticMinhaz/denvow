from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Category, SubCategory, Product


class UserUpdateForm(UserChangeForm):
    password = None  # Exclude the password field

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['image', 'name', 'category', 'description']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter Category based on the logged-in user
        self.fields['category'].queryset = Category.objects.filter(owner=user)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'name', 'category', 'sub_category', 'description']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter Category based on the logged-in user
        self.fields['category'].queryset = Category.objects.filter(owner=user)

        # Filter Sub-Category based on the logged-in user
        self.fields['sub_category'].queryset = SubCategory.objects.filter(owner=user)
