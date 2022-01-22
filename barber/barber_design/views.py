from django.shortcuts import render, redirect
from barber_serwis.models import *
from .forms import CreateSkillForm, CreateVisitForm, RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout


def user_view(request):
    return render(request, "user_view.html") 

def get_skills_view(request):
    skills = Skills.objects.all()
    return render(request, "get_skills_view.html", {"skills":skills})

def create_skill(request):
    if request.method == 'POST':
        form = CreateSkillForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CreateSkillForm()
    return render(request, "create_skill.html", {"form":form})

def delete_skill(request, id):
    skill = Skill.objects.get(id=id)
    skill.delete()
    return redirect("skills_list")

def create_visit(request):
    if request.method == 'POST':
        form = CreateVisitForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CreateVisitForm()
    return render(request, "create_skill.html", {"form":form})

def get_visits_view(request):
    visits = Visit.objects.all()
    return render(request, "get_visits_view.html", {"visit":visits})

def delete_visit(request, id):
    visit = Visit.objects.get(id=id)
    visit.delete()
    return redirect("visits_list")

def register_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        data = request.POST
        if request.POST["staff"] == "on":
            barber = Barber.objects.create(username = data['username'], password = data['password'], staff = True, email = data['email'])
            barber.save()
            redirect("user_view")
        else:
            client = Client.objects.create(username = data['username'], password = data['password'], staff = False, email = data['email'])
            client.save()
    return render(request, "register_view.html", {"register":form})

def login_view(request):
    form = LoginForm()
    context = {"login":form}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect("user_view")
        else:
            context = {"info":"Logowanie się nie powiodło.", "login":form}
    return render(request, 'login_view.html', context)
