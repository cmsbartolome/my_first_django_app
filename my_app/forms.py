from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from my_app.models import UserProfileInfo, Notes
from django.core.validators import validate_email


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(), required=True)
    email = forms.EmailField(widget=forms.EmailInput(), required=True)
    password = forms.CharField(
    widget=forms.PasswordInput(), required=True, min_length=10, max_length=100)
    first_name = forms.CharField(widget=forms.TextInput(), required=True)
    last_name = forms.CharField(widget=forms.TextInput(), required=True)

    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')


class NotesForm(forms.ModelForm):
    STATUS = (
    ('Active','active'),
    ('In-active','in-active')
    )
    description = forms.CharField(widget=forms.Textarea)
    title = forms.CharField(widget=forms.TextInput(), required=True)
    status = forms.CharField(widget=forms.Select(choices=STATUS), required=True)

    class Meta():
        model = Notes
        fields = ('description','title','status')
