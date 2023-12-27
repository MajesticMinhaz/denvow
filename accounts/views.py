from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .forms import MySignupForm
from allauth.account.views import LoginView, SignupView, LogoutView, PasswordChangeView


# Create your views here.
class MyLoginView(LoginView):
    template_name = 'accounts/pages/login.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Signin!"
        context["app_name"] = settings.APP_NAME
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Add your success message here
        messages.success(self.request, 'You have successfully logged in!')

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # Iterate over form errors and add them to messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error: {error}')
        return response
   

class MySignupView(SignupView):
    template_name = 'accounts/pages/signup.html'
    form_class = MySignupForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Signup!"
        context["app_name"] = settings.APP_NAME
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Add your success message here
        messages.success(self.request, 'You have successfully signed up!')

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # Iterate over form errors and add them to messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error: {error}')
        return response
   


class MyLogoutView(LogoutView):
    template_name = 'accounts/pages/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Logout!"
        context["app_name"] = settings.APP_NAME
        return context


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/pages/change-password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Change Password"
        context["app_name"] = settings.APP_NAME
        return context

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.

        Using this instead of just defining the success_url attribute
        because our url has a dynamic element.
        """
        success_url = reverse('profile', kwargs={'username': self.request.user.username})
        return success_url
    

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Add your success message here
        messages.success(self.request, 'You have successfully changed the password!')

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # Iterate over form errors and add them to messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error: {error}')
        return response
