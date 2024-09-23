from django.shortcuts import render

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
    
    return render(request, 'frontend/auth/register.html', context)