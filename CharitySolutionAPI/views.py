from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from CharitySolutionAPI.models import Person


def homepage(request):
    person_data = Person.objects.all()[::-1]
    return render(request, 'index.html', context={'context': person_data})


def save_user_info(request):
    user = Person(name=request.POST.get("name"),
                  age=request.POST.get("age"))
    user.save()
    return redirect('/')


def registration(request):
    return render(request, 'post_info.html')


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
