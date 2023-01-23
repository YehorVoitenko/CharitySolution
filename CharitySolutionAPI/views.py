from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from CharitySolutionAPI.models import Person


def user_list(request):
    person_data = Person.objects.all()[::-1]
    return render(request, 'user_list.html', context={'context': person_data})


def save_user_info(request):
    try:
        user = Person(name=request.POST.get("name"),
                      age=request.POST.get("age"))
        user.save()
    except ValueError:
        return redirect('/error')
    return redirect('/get_users_list')


def registration(request):
    return render(request, 'registration.html')


def error(request):
    return render(request, 'error.html')


def login_user(request):
    if request.method['POST']:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('')
            ...
        else:
            # Return an 'invalid login' error message.
            ...
    else:
        return render(request, 'login.html')
