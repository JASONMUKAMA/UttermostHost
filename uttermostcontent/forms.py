# forms.py
import logging

import dns.resolver
import re
import requests
from bootstrap_datepicker_plus.widgets import DatePickerInput
from ckeditor.widgets import CKEditorWidget
from django import forms
import datetime
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
# from django.forms import *
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField, PasswordResetForm,
)
from django.http import request

from uttermostcontent.models import *
from django.utils.translation import gettext, gettext_lazy as _
from django.forms import ModelForm, DateInput


class PersonForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = ["Profession", "country", "city", "Job", "AdditionalComment", "ResumeUpload", "CoverletterUpload"]
        exclude = ('status', 'ApprovalUpload', 'Approvalmessage')
        labels = {
            "Profession": "Profession Currently",
            "country": "Country",
            "city": "City",
            "Job": "Job",
            "AdditionalComment": "Additional Comment",
            "ResumeUpload": "Resume Upload",
            "CoverletterUpload": "Cover letter Upload",
        }
        widgets = {
            "Profession": forms.TextInput(attrs={"class": "form-control form-control-md"}),
            "Job": forms.Select(attrs={"class": "form-control form-control-md", "required": "True"}),
            "country": forms.Select(attrs={"class": "form-control form-control-md", "required": "True"}),
            "city": forms.Select(attrs={"class": "form-control form-control-md", "required": "True"}),
            "AdditionalComment": forms.Textarea(attrs={"class": "form-control w-50"}),
            "ResumeUpload": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "CoverletterUpload": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


class ContactForms(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ["Name", "Email", "Message", "PhoneNumber"]
        labels = {
            "Name": "Name",
            "Email": "Email",
            "Message": "Message",
            "PhoneNumber": "PhoneNumber",

        }
        widgets = {
            "Name": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            "Email": forms.EmailInput(attrs={"class": "form-control form-control-lg", "placeholder": "user@xxx.com"}),
            "Message": forms.Textarea(
                attrs={"class": "form-control form-control-sm", "id": "Txtmessagecontact"}),
            "PhoneNumber": forms.NumberInput(attrs={"class": "form-control form-control-lg"}),
        }

    def clean_PhoneNumber(self):
        phone_number = self.cleaned_data.get('PhoneNumber')
        if phone_number is not None:
            phone_number_str = str(phone_number)
            # Check if the phone number is an integer and non-negative
            try:
                phone_number = int(phone_number)
                if phone_number < 0:
                    raise forms.ValidationError("Phone number must be a positive integer.")
            except ValueError:
                raise forms.ValidationError("Phone number must be an integer.")

            # Validate length and digits
            if not re.match(r'^\d{10}$', phone_number_str):
                raise forms.ValidationError("Phone number must be 10 digits.")
        return phone_number


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    model = forms.ChoiceField(choices=[
        ('User', 'User'),
        ('Country', 'Country'),
        ('City', 'City'),
        ('Job', 'Job'),
        # Add other models here
    ])


logger = logging.getLogger(__name__)


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already subscribed.')

        return email


# Default user creation form
class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "password"})
    )
    password2 = forms.CharField(
        label="Confirm Password (again)",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "confirm password"}),
    )
    birthdate = forms.DateField(
        widget=forms.DateInput(
            format='%dd/%mm/%yyyy',
            attrs={'type': 'date', "class": "form-control form-control-md",
                   "required": "True"},

        ))

    class Meta:
        model = User
        fields = ["birthdate", "username", "address", "phone", "user_avatar", "first_name", "last_name", "email"]
        labels = {
            "birthdate": "Date of Birth",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "address": "address",
            "phone": "phone",
            "user_avatar": "profile picture",

        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            "first_name": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            "last_name": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            "address": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            "phone": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            "user_avatar": forms.FileInput(attrs={"class": "form-control form-control-lg"}),
            "email": forms.EmailInput(attrs={"class": "form-control form-control-lg", "placeholder": "email"}),
        }

        def __init__(self):
            self.cleaned_data = None

        def clean_birthdate(self):
            dates = self.cleaned_data['birthdate']
            age = (date.today() - dates).days / 365
            if dates > date.today():  # 🖘 raise error if greater than
                raise forms.ValidationError("The date of birth cannot be in the future!")

            if age < 18:
                raise forms.ValidationError('You must be at least 18 years old')
            return dates


# Default authentication form
class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "autofocus": True, "class": "form-control form-control-lg  text-white bg-info",
                "type": "text",
            })

    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password",
                   "placeholder": "Password",
                   "class": "form-control form-control-lg  text-white bg-info",
                   "type": "password",

                   }
        ),
    )

# class CustomPasswordResetForm(PasswordResetForm):
#     email = forms.EmailField(
#         label=("Email"),
#         max_length=254,
#         widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'custom-class'}),
#     )


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['bio', 'location', 'birth_date']
