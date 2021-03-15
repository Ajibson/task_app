from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class taskForm(ModelForm):

    class Meta:
        model = task
        fields = '__all__'

class user_signup(ModelForm):

    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        for i in User.objects.filter(username=username):
            if username == i.username:
                raise ValidationError(_("Username not available"))
        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')
        for i in User.objects.filter(email=email):
            if email == i.email:
                raise ValidationError(_("Email already used!"))
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if int(len(password)) < int(8):
            raise ValidationError(_('Password length should be up to 8'))
        elif not any(char.isdigit() for char in password):
            raise ValidationError(_('Password should contains figures'))
        elif not any(char.isalpha() for char in password):
            raise ValidationError(_('Password should has letters'))
        return password


class loginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(),max_length=20)

class ResetForms(forms.Form):
    email = forms.EmailField()

class NewPasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if int(len(password1)) < int(8):
            raise ValidationError(_('Password length should be up to 8'))
        elif not any(char.isdigit() for char in password1):
            raise ValidationError(_('Password should contains at least one number'))
        elif not any(char.isalpha() for char in password1):
            raise ValidationError(_('Password should has letters'))
        return password1
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get('password2')
        if str(password1) != str(password2):
            raise ValidationError(_("Passwords do not match"))
        return password2


class usersForm(ModelForm):

    password = forms.PasswordInput()

    class Meta:
        model = users
        fields = ('email', 'username')

