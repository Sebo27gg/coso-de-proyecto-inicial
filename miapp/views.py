from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Allergy, Product

# Create your views here.

# Index: pagina principal de informacion
def index(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, 'index.html')

#Home: Buscador de alimentos
def home(request):  
    query = request.GET.get('search')

    if query:
        products_list = Product.objects.filter(name__icontains=query)
    else:
        products_list = Product.objects.all()

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_allergies = user.allergy_set.all()
    else:
        allergy_list = Allergy.objects.all()
        user_allergies = []
        for id in list(request.GET)[:-1]:
            user_allergies.append(Allergy.objects.get(id=int(id)))
                      
    banned_products = []
    for product in products_list:
        for ingredient in product.ingredients.all():    
            for allergy in user_allergies:
                if ingredient in allergy.ingredients.all():
                    banned_products.append(product)

    return render(request, 'home.html', {
        "allergies": user_allergies if request.user.is_authenticated else allergy_list,
        "query": query,
        "products" : products_list,
        "banned" : banned_products
        })

#Signup: Creacion de cuenta
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

#Signin: entrar con cuenta propia
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

#Perfil: gestor de alergias, y demas configuraciones        
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
    
#Signout: Vista especial para salir de tu cuenta
@login_required 
def signout(request):
    logout(request)
    return redirect("index")

#Product detail: Detalles de un producto en particular
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    ingredient_list = product.ingredients.all()
    return render(request, 'product_detail.html',  {
        'product': product,
        'ingredients': ingredient_list,
    })