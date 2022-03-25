from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm, User, UserPasswordForm
from django.contrib.auth import update_session_auth_hash

@login_required
def account_edit_password(request):
    confirm = ''
    if request.method == "POST":
        form = UserPasswordForm(request.POST)
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm-password', '')

        if password == '':
            messages.error(request, 'Password cannot be empty.')
        elif password != confirm:
            messages.error(request, 'Password does not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            if form.is_valid():
                user = User.objects.get(pk=request.user.pk)
                user.set_password(password)
                update_session_auth_hash(request, user)
                user.save()
                messages.success(request, 'Password has been successfully updated.')
                return redirect('account-edit')
    else:
        form = UserPasswordForm()


    context = {
        'nav_active': 'account',
        'confirm': confirm,
        'form': form
    }
    return render(request, 'accounts/edit-password.html', context=context)

@login_required
def account_edit(request):

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(email=request.user.email):
                messages.error(request, 'Email Already Exists.')
            else:
                user = User.objects.get(pk=request.user.pk)
                user.email = email
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                messages.success(request, 'Account details updated.')
                form.save(commit=False)
                user.save()
                return redirect('account-edit')
    else:
        form = UserForm(instance=request.user)

    context = {
        'form': form,
        'nav_active': 'account',
    }
    return render(request, 'accounts/edit.html', context=context)

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

