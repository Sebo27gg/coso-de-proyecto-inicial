from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Allergy, Product
from django.db.models import Q

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
def perfil(request):
    allergy_list = Allergy.objects.all()
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        user_list = user.allergy_set.all()
        return render(request, 'perfil.html', {"allergies" : allergy_list, "user_allergies" : user_list})
    else:
        for allergy in allergy_list:
            if str(allergy.id) in list(request.POST):
                user.allergy_set.add(allergy)
            else:
                user.allergy_set.remove(allergy)
        user.save()
        return redirect("home")
   
@login_required 
def signout(request):
    logout(request)
    return redirect("index")

def product_list(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'product_list.html', {
        'products': products,
        'query': query,
    })

def product_detail(request, slug):
    # Busca el producto por su slug. Si no lo encuentra, arroja un error 404.
    product = get_object_or_404(Product, slug=slug)
    ingredients_list = product.ingredients.all()
    return render(request, 'product_detail.html',  {
        'product': product,
        'ingredients': ingredients_list,
    })