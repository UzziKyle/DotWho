from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegistrationForm, ProfileForm


# Create your views here.
def sign_in(request):
    context = {}
    
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        
        context['form'] = LoginForm()
            
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user)
                return redirect('home')
            
        context['form'] = form
            
    return render(request, 'profiles/login.html', context)


def sign_out(request):
    logout(request)
    return redirect('home')


def sign_up(request):
    context = {}
    
    if request.method == 'GET':
        context['form'] = RegistrationForm()

    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        
        context['form'] = form
        
    return render(request, 'profiles/register.html', context)
        
