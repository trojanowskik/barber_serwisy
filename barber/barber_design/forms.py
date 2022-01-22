from django import forms
from django.contrib.admin import widgets
from django.contrib.auth import authenticate
from barber_serwis.models import Skills, Visit, User

class CreateSkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'

class CreateVisitForm(forms.ModelForm):
    date = forms.DateField(widget = forms.SelectDateWidget)
    time = forms.TimeField()#widget = forms.TimeInput(format = '%H:%M')
    class Meta:
        model = Visit
        fields = '__all__'

class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=255)
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=128)
    token = forms.HiddenInput()
    staff = forms.BooleanField()

class LoginForm(forms.Form):
    email = forms.CharField(max_length=255)
    password = forms.CharField(widget = forms.PasswordInput)