from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class AuthForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=200)

class TalkForm(forms.Form):
    text = forms.CharField(max_length=200)


class TalkAnswerForm(forms.Form):
    text = forms.CharField(max_length=300)