from account.forms import *
from account.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticated_user = authenticate(request, username=user.email, password=form.cleaned_data['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'User registered and logged in successfully.')
                return redirect('auth:login')
            else:
                error_message = 'User registration failed. '
                for field, errors in form.errors.items():
                    error_message += f"{field}: {', '.join(errors)}. "
                messages.error(request, error_message.strip())
        else:
            error_message = 'User registration failed. '
            for field, errors in form.errors.items():
                error_message += f"{field}: {', '.join(errors)}. "
            messages.error(request, error_message.strip())
    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }
    
    return render(request, 'auth/register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('frontend:home')
            else:
                error_message = 'Invalid email or password.'
                for field, errors in form.errors.items():
                    error_message += f"{field}: {', '.join(errors)}. "
                messages.error(request, error_message.strip())
        else:
            error_message = 'Login failed. Please check your input.'
            for field, errors in form.errors.items():
                error_message += f"{field}: {', '.join(errors)}. "
            messages.error(request, error_message.strip())
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'auth/login.html', context)