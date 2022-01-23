from django import forms
from django.contrib.auth import authenticate
from django.test import client
from barber_serwis.models import Barber, Skills, Visit, User

class CreateSkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'

class CreateVisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['date', 'time', 'skills', 'client']
    
    

class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=255)
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=128)
    token = forms.HiddenInput()
    staff = forms.BooleanField(required = False)

class LoginForm(forms.Form):
    email = forms.CharField(max_length=255)
    password = forms.CharField(widget = forms.PasswordInput)

class SetSkillForm(forms.ModelForm):
    class Meta:
        model = Barber
        fields = ('skills', )
