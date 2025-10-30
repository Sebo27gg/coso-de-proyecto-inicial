from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index, name="index"),
    path('home/', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.signin, name="login"),
    path('logout/', views.signout, name="logout"),
    path('settings/', views.perfil, name="perfil"),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]

