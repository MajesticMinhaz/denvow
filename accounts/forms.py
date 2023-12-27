# forms.py
from allauth.account.forms import SignupForm
from django import forms


class MySignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30, 
        label='First Name', 
        required=True, 
        widget=forms.TextInput(
            attrs={'placeholder': 'First name', 'autocomplete': 'first_name'}
        )
    )

    last_name = forms.CharField(
        max_length=30, 
        label='Last Name', 
        required=True, 
        widget=forms.TextInput(
            attrs={'placeholder': 'Last name', 'autocomplete': 'last_name'}
        )
    )

    privacy_policy = forms.BooleanField(
        label='Privacy Policy',
        required=True,
        widget=forms.CheckboxInput(),
    )
