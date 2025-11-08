from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Allergy, Product, Ingredient
from django.core.paginator import Paginator
from django.db.models import Q
from urllib.parse import urlparse

# Create your views here.

# Index: pagina principal de informacion
def index(request):
    return render(request, 'index.html')

#Home: Buscador de alimentos
def home(request): 
    # Logica de interfaz de productos y paginacion
    search_query = request.GET.get('search')
    page_num = request.GET.get('page')
    view_filter = request.GET.get('view_filter', 'todos')
    search_scope = request.GET.get('search_scope', 'todos') 
    
    query = '&'.join([f'{param}={value}' for param, value in request.GET.items() if param != "page"])

    if not page_num:
        page_num = 1

    #Filtro busqueda
    if search_query:
        if search_scope == 'productos':
            # Solo buscar en el nombre del producto
            products_list = Product.objects.filter(
                Q(name__icontains=search_query)
            ).distinct()
        elif search_scope == 'ingredientes':
            # Solo buscar en los ingredientes
            products_list = Product.objects.filter(
                Q(ingredients__name__icontains=search_query)
            ).distinct()
        else: # 'todos'
            # Buscar en ambos (lógica original)
            products_list = Product.objects.filter(
                Q(name__icontains=search_query) |
                Q(ingredients__name__icontains=search_query)
            ).distinct()
    else:
        products_list = Product.objects.all()

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_allergies = user.allergy_set.all()
    else:
        allergy_list = Allergy.objects.all()
        user_allergies = []
        for key in request.GET:
            if key.isnumeric():
                try:
                    user_allergies.append(Allergy.objects.get(id=int(key)))
                except Allergy.DoesNotExist:
                    pass

    # Logica de alimentos baneados

    banned_ingredients = set()
    for allergy in user_allergies:
        banned_ingredients.update(allergy.ingredients.all())
    
    banned_products = []
    for product in products_list: 
        if set(product.ingredients.all()) & banned_ingredients:
            banned_products.append(product)

   #Filtro de permitidos/prohibidos/todos
    if view_filter == 'permitidos':
        final_products_list = [p for p in products_list if p not in banned_products]
    elif view_filter == 'prohibidos':
        final_products_list = [p for p in products_list if p in banned_products]
    else:
        final_products_list = products_list


    products_page = Paginator(final_products_list, 18).get_page(page_num)

    return render(request, 'home.html', {
        "allergies": user_allergies if request.user.is_authenticated else allergy_list,
        "search": search_query,
        "products" : products_page,
        "banned" : banned_products,
        "view_filter": view_filter,
        "search_scope": search_scope, # <-- NUEVO: Pasa el filtro a la plantilla
        "query": query
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
    home_url = request.META.get('HTTP_REFERER')
    if home_url:
        parsed_url = urlparse(home_url)
        home_query = '?' + parsed_url.query 
    else:
        home_query = ''
    product = get_object_or_404(Product, slug=slug)
    ingredient_list = product.ingredients.all()
    return render(request, 'product_detail.html',{
        'product': product,
        'ingredients': ingredient_list,
        'query': home_query
    })    

@login_required 
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        user = request.user
        
        # Asumiendo que el related_name es 'favorite_products'
        if user.favorite_products.filter(id=product_id).exists():
            user.favorite_products.remove(product)
        else:
            user.favorite_products.add(product)
            
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required 
def view_favorites(request):
    favorites = request.user.favorite_products.all()
    return render(request, 'favorites.html', {
        'favorites': favorites
    })