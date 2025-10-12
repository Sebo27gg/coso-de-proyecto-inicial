from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'registration/signin.html', {"form": UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("home")
            except:
                return render(request, 'registration/signin.html', {
                    "form": UserCreationForm(),
                    "msg": "Nombre de usuario ya existente"
                })
        return render(request, 'registration/signin.html', {
            "form" : UserCreationForm(),
            "msg" : "Las contraseñas no coinciden"
        })
    
@login_required 
def signout(request):
    logout(request)
    return redirect("index")
