from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Allergy

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, 'index.html')

def home(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        list = user.allergy_set.all()
    else:
        list = Allergy.objects.all()
    return render(request, 'home.html', {"list": list})

def signup(request):
    if request.method == 'GET':
        return render(request, 'registration/signup.html', {"form": CustomUserCreationForm()})
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("home")   
        else:
            return render(request, 'registration/signup.html', {
                "form" : CustomUserCreationForm(),
                "msg" : "error: compruebe que las contraseñas no coincidan o que el nombre de usuario no este en uso"
            })

def signin(request):
     if request.method == 'GET':
        return render(request, 'registration/login.html', {"form": AuthenticationForm()})
     else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])

        if user is None:
            return render(request, 'registration/login.html', {
                "form": AuthenticationForm(),
                "msg": "el usuario o la contraseña estan incorrectos"
            })
        else:
            login(request, user)
            return redirect("home")
     
@login_required 
def signout(request):
    logout(request)
    return redirect("index")
