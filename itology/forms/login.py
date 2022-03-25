from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from marshmallow import ValidationError

from itology.config import ACCOUNT_TYPE, USER_TYPE
from itology.models import Client

PASSWORD_FIELDS = {'data-toggle': 'password', 'id': 'password'}
FORM_CONTROL = {'class': 'form-control'}
FORM_CONTROL_FILE = {'class': 'form-control-file'}


def _attrs(placeholder):
    return {'placeholder': placeholder} | FORM_CONTROL


def _validate_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError(f'{email} already exists', params={'email': email})


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs=_attrs('Username')))
    email = forms.EmailField(required=True, validators=[_validate_email], widget=forms.TextInput(attrs=_attrs('Email')))
    user_type = forms.CharField(required=True, widget=forms.RadioSelect(choices=USER_TYPE))
    account_type = forms.CharField(required=True, widget=forms.RadioSelect(choices=ACCOUNT_TYPE))
    password1 = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs=_attrs('Password') | PASSWORD_FIELDS
        ))
    password2 = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs=_attrs('Confirm Password') | PASSWORD_FIELDS
        ))

    def save(self, commit=True):
        user_type = self.cleaned_data['user_type']
        account_type = self.cleaned_data['account_type']

        user = super(RegisterForm, self).save(commit=True)
        client = Client.objects.create(user=user)
        client.user_type = user_type
        client.account_type = account_type
        client.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs=_attrs('Username')))
    password = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs=_attrs('Password') | PASSWORD_FIELDS | {'name': 'password'}
        ))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs=FORM_CONTROL))
    email = forms.EmailField(required=True, validators=[_validate_email], widget=forms.TextInput(attrs=FORM_CONTROL))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateClientForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs=FORM_CONTROL_FILE))

    class Meta:
        model = Client
        fields = ['avatar']
