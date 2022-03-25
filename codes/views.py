from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import AllCodesForm, Codes, AllCodes, Category


@login_required
def home(request):
    return render(request, 'accounts/home.html')


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)

    page = request.GET.get('page', 1)
    paginator = Paginator(categories, 10)
    try:
        categories_paginated = paginator.page(page)
    except PageNotAnInteger:
        categories_paginated = paginator.page(1)
    except EmptyPage:
        categories_paginated = paginator.page(paginator.num_pages)

    url = '?search='
    context = {
        'nav_active': 'category',
        'lists': categories_paginated,
        'pagination_url': url + '&page='
    }
    return render(request, 'category/lists.html', context)


@login_required
def new_code(request):

    if request.method == "POST":
        form = AllCodesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            categories = form.cleaned_data['category']
            body = form.cleaned_data['body']
            codes = request.POST.getlist('codes[]')

            if len(codes) >= 1:
                infos = request.POST.getlist('infos[]')
                all_codes = AllCodes.objects.create(
                    user=request.user,
                    title=title,
                    body=body
                )
                for category in categories:
                    all_codes.category.add(category)

                for i, code in enumerate(codes):
                    Codes.objects.create(
                        all=all_codes,
                        title=infos[i],
                        code=code
                    )
                form = AllCodesForm()
                messages.success(request, title + ' has been added.')
            else:
                messages.error(request, 'Please enter at least 1 code.')
    else:
        form = AllCodesForm()

    context = {
        'nav_active': 'new-code',
        'form': form,
    }
    return render(request, 'codes/new-code.html', context)


@login_required
def lists(request):
    all_codes = AllCodes.objects.filter(user=request.user)

    url = '?search='
    searched = request.GET.get('search', '')
    filtered = request.GET.getlist('f[]')
    if searched:
        all_codes = all_codes.filter(title__contains=searched)
        s = searched.split(' ')
        url += '%20'.join(s)
    if filtered:
        all_codes = all_codes.filter(category__name__in=filtered)
        for f in filtered:
            value = f.split(' ')
            url += '&f%5B%5D=' + '%20'.join(value)

    categories = Category.objects.filter(user=request.user)
    page = request.GET.get('page', 1)
    # (obj, no of objects to display)
    paginator = Paginator(all_codes, 10)
    try:
        all_codes_paginated = paginator.page(page)
    except PageNotAnInteger:
        all_codes_paginated = paginator.page(1)
    except EmptyPage:
        all_codes_paginated = paginator.page(paginator.num_pages)

    context = {
        'nav_active': 'lists',
        'lists': all_codes_paginated,
        'categories': categories,
        'searched': searched,
        'filtered': ','.join(filtered),
        'pagination_url': url + '&page=',
    }
    return render(request, 'codes/lists.html', context)


def single_code(request, pk):
    try:
        all_codes = AllCodes.objects.get(user=request.user, pk=pk)
    except AllCodes.DoesNotExist:
        raise Http404()
    codes = Codes.objects.filter(all=all_codes)

    context = {
        'nav_active': 'lists',
        'info': all_codes,
        'codes': codes,
    }
    return render(request, 'codes/code.html', context=context)

def single_code_edit(request, pk):

    try:
        all_codes = AllCodes.objects.get(user=request.user, pk=pk)
    except AllCodes.DoesNotExist:
        raise Http404()
    codes = Codes.objects.filter(all=all_codes)

    if request.method == "POST":
        form = AllCodesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            categories = form.cleaned_data['category']
            body = form.cleaned_data['body']
            codes_ = request.POST.getlist('codes[]')

            if len(codes) >= 1:
                codes.delete()
                infos = request.POST.getlist('infos[]')

                for i, code in enumerate(codes_):
                    Codes.objects.create(
                        all=all_codes,
                        title=infos[i],
                        code=code
                    )

                all_codes.title = title
                all_codes.category.set(categories)
                all_codes.body = body
                all_codes.save()
                messages.success(request, 'Successfully updated.')
                return redirect("single-code", pk=pk)
            else:
                messages.error(request, 'Please enter at least 1 code.')
    else:
        form = AllCodesForm(instance=all_codes)

    context = {
        'pk': pk,
        'form': form,
        'codes': codes,
        'code_cnt': len(codes),
        'nav_active': 'lists',
    }

    return render(request, 'codes/edit-code.html', context=context)
