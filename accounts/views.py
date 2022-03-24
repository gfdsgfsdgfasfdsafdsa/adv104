from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def register(request):
    return render(request, 'accounts/register.html')


def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')

        user = authenticate(request, username=username,
                            password=request.POST.get('password'))

        if user is not None:
            login(request, user)
            return redirect('lists')
        else:
            messages.info(request, 'Username/Password is incorrect.')
            return render(request, 'accounts/login.html')
    elif request.user.is_authenticated:
        return redirect('lists')

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

