from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import UserUpdateForm, SubCategoryForm, ProductForm
from .models import Profile, Category, SubCategory, Product
from .sidebar import sidebar_data
from .page_title import page_title_data


# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/pages/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=1)
        context["page_title_data"] = page_title_data(name='Dashboard', path_sequence=['Home', 'Dashboard'])
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['profile_pic', 'job_title', 'about', 'facebook', 'instagram', 'twitter', 'linkedin']

    template_name = 'dashboard/pages/profile.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        # Update Profile instance
        instance = form.save(commit=False)
        instance.save()

        # Update User instance
        user_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()

        response = super().form_valid(form)
        messages.success(self.request, 'Profile Updated successfully!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(self.request, f'Error: {error}')
                else:
                    field_name = form.fields[field].label
                    messages.error(self.request, f'Error in {field_name}: {error}')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add user-related data to the context
        user_form = UserUpdateForm(instance=self.request.user)
        context["user_form"] = user_form

        context["title"] = "Profile"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=9)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'User', context['title']])
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['image', 'name', 'description']
    template_name = 'dashboard/pages/product-management/create.html'
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        # Set the owner before calling form validation
        form.instance.owner = self.request.user

        response = super().form_valid(form)
        messages.success(self.request, 'Category created successfully!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(self.request, f'Error: {error}')
                else:
                    field_name = form.fields[field].label
                    messages.error(self.request, f'Error in {field_name}: {error}')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Create Category"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=1)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'dashboard/pages/product-management/list.html'
    ordering = ['name']  # Add this line to order by name

    def get_queryset(self):
        # Filter categories based on the currently logged-in user
        return Category.objects.filter(owner=self.request.user).order_by(*self.ordering)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Specify the desired order of fields
        field_order = ['id', 'image', 'name', 'description', 'last_update']

        # Get model fields
        model_fields = [Category._meta.get_field(field_name) for field_name in field_order]

        context["model_fields"] = model_fields

        context['create_url'] = 'category_create'
        context['update_url'] = 'category_update'
        context['delete_url'] = 'category_delete'

        context["title"] = "Categories"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=1)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'image', 'description']
    template_name = 'dashboard/pages/product-management/update.html'
    success_url = reverse_lazy('categories')

    def get_queryset(self):
        # Only allow the owner to update their own categories
        return Category.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        # Set the owner before calling form validation
        form.instance.owner = self.request.user

        response = super().form_valid(form)
        messages.success(self.request, 'Category Updated successfully!')
        return response

    def get_object(self, queryset=None):
        # Ensure the object being updated belongs to the current user
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to update this category.")
        return obj

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(self.request, f'Error: {error}')
                else:
                    field_name = form.fields[field].label
                    messages.error(self.request, f'Error in {field_name}: {error}')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Category Update"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=1)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'dashboard/pages/product-management/delete.html'
    success_url = reverse_lazy('categories')

    def get_queryset(self):
        # Only allow the owner to delete their own categories
        return Category.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        # Ensure the object being deleted belongs to the current user
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this category.")
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category Deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Category Delete"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=1)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class SubCategoryCreateView(LoginRequiredMixin, CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'dashboard/pages/product-management/create.html'
    success_url = reverse_lazy('sub_categories')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Set the owner before calling form validation
        form.instance.owner = self.request.user

        response = super().form_valid(form)
        messages.success(self.request, 'Subcategory created successfully!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(self.request, f'Error: {error}')
                else:
                    field_name = form.fields[field].label
                    messages.error(self.request, f'Error in {field_name}: {error}')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sub-Category Create"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=2)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class SubCategoryListView(LoginRequiredMixin, ListView):
    model = SubCategory
    template_name = 'dashboard/pages/product-management/list.html'
    ordering = ['name']  # Add this line to order by name

    def get_queryset(self):
        # Filter sub categories based on the currently logged-in user
        return SubCategory.objects.filter(owner=self.request.user).order_by(*self.ordering)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Specify the desired order of fields
        field_order = ['id', 'image', 'name', 'category','description', 'last_update']

        # Get model fields
        model_fields = [SubCategory._meta.get_field(field_name) for field_name in field_order]

        context["model_fields"] = model_fields

        context['create_url'] = 'sub_category_create'
        context['update_url'] = 'sub_category_update'
        context['delete_url'] = 'sub_category_delete'
        context["title"] = "Sub-Categories"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=2)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class SubCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'dashboard/pages/product-management/update.html'
    success_url = reverse_lazy('sub_categories')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_queryset(self):
        # Only allow the owner to update their own categories
        return SubCategory.objects.filter(owner=self.request.user)
    
    def get_object(self, queryset=None):
        # Ensure the object being updated belongs to the current user
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to update this sub-category.")
        return obj

    def form_valid(self, form):
        # Set the owner before calling form validation
        form.instance.owner = self.request.user

        response = super().form_valid(form)
        messages.success(self.request, 'Subcategory updated successfully!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(self.request, f'Error: {error}')
                else:
                    field_name = form.fields[field].label
                    messages.error(self.request, f'Error in {field_name}: {error}')
        return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Sub-Category Update"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=2)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class SubCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = SubCategory
    template_name = 'dashboard/pages/product-management/delete.html'
    success_url = reverse_lazy('sub_categories')

    def get_queryset(self):
        # Only allow the owner to delete their own sub-categories
        return SubCategory.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        # Ensure the object being deleted belongs to the current user
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this sub-category.")
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Sub-Category Deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sub-Category Delete"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=2)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/pages/product-management/create.html'
    success_url = reverse_lazy('products')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Set the owner before calling form validation
        form.instance.owner = self.request.user

        response = super().form_valid(form)
        messages.success(self.request, 'Product created successfully!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(self.request, f'Error: {error}')
                else:
                    field_name = form.fields[field].label
                    messages.error(self.request, f'Error in {field_name}: {error}')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Product Create"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=3)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'dashboard/pages/product-management/list.html'
    ordering = ['name']  # Add this line to order by name

    def get_queryset(self):
        # Filter sub categories based on the currently logged-in user
        return Product.objects.filter(owner=self.request.user).order_by(*self.ordering)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Specify the desired order of fields
        field_order = ['id', 'image', 'name', 'category', 'sub_category', 'description', 'last_update']

        # Get model fields
        model_fields = [Product._meta.get_field(field_name) for field_name in field_order]

        context["model_fields"] = model_fields

        context["title"] = "Products"
        context['create_url'] = 'product_create'
        context['update_url'] = 'product_update'
        context['delete_url'] = 'product_delete'
        context["app_name"] = settings.APP_NAME
        context["has_search_bar"] = True
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=3)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/pages/product-management/update.html'
    success_url = reverse_lazy('products')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_queryset(self):
        # Only allow the owner to update their own categories
        return Product.objects.filter(owner=self.request.user)
    
    def get_object(self, queryset=None):
        # Ensure the object being updated belongs to the current user
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to update this product.")
        return obj

    def form_valid(self, form):
        # Set the owner before calling form validation
        form.instance.owner = self.request.user

        response = super().form_valid(form)
        messages.success(self.request, 'Product updated successfully!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(self.request, f'Error: {error}')
                else:
                    field_name = form.fields[field].label
                    messages.error(self.request, f'Error in {field_name}: {error}')
        return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Product Update"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=3)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'dashboard/pages/product-management/delete.html'
    success_url = reverse_lazy('products')

    def get_queryset(self):
        # Only allow the owner to delete their own product
        return Product.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        # Ensure the object being deleted belongs to the current user
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this product.")
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product Deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Product Delete"
        context["app_name"] = settings.APP_NAME
        context["sidebar_data"] = sidebar_data(section_active_id=3, sub_section_active_id=3)
        context["page_title_data"] = page_title_data(name=context['title'], path_sequence=['Home', 'Product Management', context['title']])
        return context


class NotFoundView(TemplateView):
    template_name = "dashboard/pages/404.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard"
        context["app_name"] = settings.APP_NAME
        return context


    @classmethod
    def get_rendered_view(cls):
        as_view_fn = cls.as_view()

        def view_fn(request):
            response = as_view_fn(request)
            response.render()
            return response

        return view_fn
