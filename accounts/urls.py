from django.urls import path
from .views import MyLoginView, MySignupView, MyLogoutView, MyPasswordChangeView


urlpatterns = [
    path('login/', MyLoginView.as_view(), name='account_login'),
    path('signup/', MySignupView.as_view(), name='account_signup'),
    path('logout/', MyLogoutView.as_view(), name='account_logout'),
    path('password/change/', MyPasswordChangeView.as_view(), name='account_change_password')
]
