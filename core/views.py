from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Recipe
from django.contrib import messages
from .forms import RecipeForm, CommentForm, CustomUserForm, CustomUserCreationForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import get_user_model

def home(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    featured_recipes = Recipe.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]
    return render(request, 'home.html', {'recipes': recipes, 'featured_recipes': featured_recipes})

def about(request):
    return render(request, 'about.html')

def recipies(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipies.html', {'recipes': recipes})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # or redirect to any other page
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in user after signup
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def view_profile(request):
    return render(request, 'view_profile.html', {'user_obj': request.user})

User = get_user_model()

@login_required
def public_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    recipes = profile_user.recipes.all().order_by('-created_at')

    context = {
        'profile_user': profile_user,
        'recipes': recipes,
    }
    return render(request, 'public_profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

def add_recipe(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {'form': form})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.recipe = recipe
            new_comment.save()
            return redirect('recipe_detail', pk=pk)
    else:
        form = CommentForm()

    context = {
        'recipe': recipe,
        'form': form,
        'comments': comments,
    }
    return render(request, 'recipe_detail.html', context)

@login_required
def toggle_like(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user in recipe.likes.all():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)
    return redirect('recipe_detail', pk=pk)

@login_required
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if request.user in target.followers.all():
        target.followers.remove(request.user)
    else:
        target.followers.add(request.user)
    return redirect('public_profile', username=target.username)