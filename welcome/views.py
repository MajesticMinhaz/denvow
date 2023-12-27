from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView
from .models import TeamMember
from .forms import ContactForm


# Create your views here.
class WelcomeView(ListView, FormView):
    template_name = 'welcome/index.html'
    model = TeamMember
    context_object_name = 'items'
    
    # Filter TeamMember objects based on the existence of a related Profile
    queryset = TeamMember.objects.filter(profile__user__isnull=False)

    form_class = ContactForm
    success_url = reverse_lazy('account_signup')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Welcome!"
        context["app_name"] = settings.APP_NAME
        return context
    
    def form_valid(self, form):
        # Process the form data here
        # You can access the form data using form.cleaned_data
        # For example, save the form data to the database
        form.save()
        return super().form_valid(form)


class TermsOfServiceView(TemplateView):
    template_name = 'welcome/pages/terms-of-service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Terms of Service!"
        context["app_name"] = settings.APP_NAME
        return context

    