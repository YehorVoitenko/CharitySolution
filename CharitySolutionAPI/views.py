from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from CharitySolutionAPI.models import Person


def items_list(request):
    if request.user.is_authenticated:
        person_data = Person.objects.all()[::-1]
        return render(request, 'items_list.html', context={'context': person_data})
    else:
        return redirect('/error')


def save_item_info(request):
    try:
        if request.method == 'POST':
            user = Person(name=request.POST.get("name"),
                          age=request.POST.get("age"))
            user.save()
    except ValueError:
        return redirect('/error')
    return redirect('/get_items_list')


def add_item(request):
    if request.user.is_authenticated:
        return render(request, 'add_item.html')
    else:
        return redirect('/error')


def error(request):
    return render(request, 'error.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/get_items_list')
        else:
            return redirect('/error')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/login_user')
