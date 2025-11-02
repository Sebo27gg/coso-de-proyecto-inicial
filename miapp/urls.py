from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index, name="index"),
    path('home/', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.signin, name="login"),
    path('logout/', views.signout, name="logout"),
    path('home/settings/', views.perfil, name="perfil"),
    path('home/product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('home/product/fav/', views.view_favorites, name='view_favorites'),
    path('home/product/fav/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
]

