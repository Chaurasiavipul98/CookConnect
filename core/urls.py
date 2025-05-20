
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import*

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('profile/', views.view_profile, name='profile'),

    path('user/<str:username>/', views.public_profile, name='public_profile'),
    
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('', views.home, name='home'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('add/', views.add_recipe, name='add_recipe'),

    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),

    path('like/<int:pk>/', views.toggle_like, name='toggle_like'),

    path('user/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),

    

]
