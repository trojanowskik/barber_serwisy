from django.shortcuts import render, redirect
from django.test import client
from barber_serwis.models import *
from .forms import CreateSkillForm, CreateVisitForm, RegistrationForm, LoginForm, SetSkillForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from barber_serwis.tasks import send_email

def user_view(request):
    skills = []
    if not request.user.is_authenticated:
        return redirect("login_view")
    if request.user.staff:
        user = Barber.objects.get(id = request.user.id)
        skills = user.skills.values()
    else :
        user = Client.objects.get(id = request.user.id)
    return render(request, "user_view.html", {"user":user, "skills":skills} ) 

def get_skills_view(request):
    skills = Skills.objects.all()
    return render(request, "get_skills_view.html", {"skills":skills})

def create_skill(request):
    if not request.user.is_authenticated:
        return redirect("login_view")
    if not request.user.staff:
        return redirect("user_view")
    if request.method == 'POST':
        form = CreateSkillForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CreateSkillForm()
    return render(request, "create_skill.html", {"form":form})

def delete_skill(request, id):
    if not request.user.is_authenticated:
        return redirect("login_view")
    if not request.user.staff:
        return redirect("user_view")
    skill = Skills.objects.get(id=id)
    try:
        skill.delete()
        return redirect("skills_list")
    except:
        context = {"info":"A specialization cannot be removed if someone has made an appointment."}
        return render(request, 'get_skills_view.html', context)
    
def delete_visit(request, id):
    if not request.user.is_authenticated:
        return redirect("login_view")
    if request.user.staff:
        return redirect("user_view")
    visit = Visit.objects.get(id=id)
    visit.delete()
    return redirect("visits_list")

def create_visit(request):
    info=""

    if not request.user.is_authenticated:
        return redirect("login_view")
    if request.user.staff:
        return redirect("user_view")

    form = CreateVisitForm(initial={'client':request.user.id})

    if request.method == "POST":
        date = request.POST["date"]
        time = request.POST["time"]+':00'
        client = Client.objects.get(id = request.user.id)
        wizyty = client.visit_set.all()
        is_exist = False
        for visit in wizyty:
            if str(date) == str(visit.date) and str(time) == str(visit.time):
                is_exist = True
                info = "Wizyta o takiej dacie i godzinie już istnieje."
        if is_exist == False:
            form = CreateVisitForm(request.POST)
            form.is_valid()
            form.save()
            info = "Twoja wizyta została dodana."
            send_email(request.user, date, time)


    return render(request, "create_visit.html", {"form":form, "info":info})

def get_visits_view(request):
    if not request.user.is_authenticated:
        return redirect("login_view")
    if request.user.staff:
        visits = Visit.objects.all()
    else:
        user = Client.objects.get(id = request.user.id)
        visits = Visit.objects.filter(client = user.id)
    return render(request, "get_visits_view.html", {"visit":visits})

def register_view(request):
    form = RegistrationForm()
    info = ""
    if request.method == 'POST':
        data = request.POST
        if "staff" in data:
            if data["staff"] == "on":
                try:
                    barber = Barber.objects.create(username = data['username'], password = data['password'], staff = True, email = data['email'])
                    barber.set_password(data['password'])
                    barber.is_valid()
                    barber.save()
                    return redirect("login_view")
                except IntegrityError:
                    info = "Taki użytkownik już istnieje."
                
        else:
            try:
                client = Client.objects.create(username = data['username'], password = data['password'], staff = False, email = data['email'])
                client.set_password(data['password'])
                client.save()
                return redirect("login_view")
            except IntegrityError:
                info = "Taki użytkownik już istnieje."
             
    return render(request, "register_view.html", {"register":form, "info":info})

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

def set_skill(request):
    if not request.user.is_authenticated:
        return redirect("login_view")
    if not request.user.staff:
        return redirect("user_view")
    form = SetSkillForm()
    user = Barber.objects.get(id = request.user.id)
    if request.method == "POST":
        id = request.POST["skills"][0]
        skill = Skills.objects.get(id = id)
        user.skills.add(skill)
        user.save()
        return redirect('user_view')
    return render(request, 'set_skill.html', {"form":form})

def delete_user_skill(request, id):
    if not request.user.is_authenticated:
        return redirect("login_view")
    if not request.user.staff:
        return redirect("user_view")
    user = Barber.objects.get(id = request.user.id)
    user.skills.remove(id)
    return redirect('user_view')

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect("login_view")
    logout(request)
    return redirect('login_view')

def main_view(request):
    return render(request, 'main.html')