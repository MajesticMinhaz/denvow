from django.urls import path
from .views import WelcomeView, TermsOfServiceView

urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome'),
    path('terms-of-serviec/', TermsOfServiceView.as_view(), name='terms-of-service')
]
