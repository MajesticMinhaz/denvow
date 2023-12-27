from django.urls import path
from .views import DashboardView
from .views import UserProfileView
from .views import CategoryCreateView, CategoryListView, CategoryUpdateView, CategoryDeleteView
from .views import SubCategoryCreateView, SubCategoryListView, SubCategoryUpdateView, SubCategoryDeleteView
from .views import ProductCreateView, ProductListView, ProductUpdateView, ProductDeleteView


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('category/create/', CategoryCreateView.as_view(), name="category_create"),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    path('sub-category/create/', SubCategoryCreateView.as_view(), name="sub_category_create"),
    path('sub-categories/', SubCategoryListView.as_view(), name='sub_categories'),
    path('sub-category/<int:pk>/update/', SubCategoryUpdateView.as_view(), name='sub_category_update'),
    path('sub-category/<int:pk>/delete/', SubCategoryDeleteView.as_view(), name='sub_category_delete'),

    path('product/create/', ProductCreateView.as_view(), name="product_create"),
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name="product_update"),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
]
