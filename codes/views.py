from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def new_code(request):

    context = {
        'nav_active': 'new-code'
    }
    return render(request, 'codes/new-code.html', context)

@login_required
def lists(request):

    context = {
        'nav_active': 'lists'
    }
    return render(request, 'codes/lists.html', context)
