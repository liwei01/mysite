#coding=utf-8

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-lg' ,'id':'id_username', 'placeholder': '用户名'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control input-lg' ,'id':'id_password', 'placeholder': '密码'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=100,
        widget=forms.TextInput(attrs={'id':'username', 'onblur': 'authentication()'}))
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

class SetInfoForm(forms.Form):
    username = forms.CharField()

class CommmentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': '60', 'rows': '6'}))

class SearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput)