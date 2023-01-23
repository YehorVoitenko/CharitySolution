from django.shortcuts import render, redirect
from CharitySolutionAPI.models import Person


def homepage(request):
    person_data = Person.objects.all()[::-1]
    return render(request, 'index.html', context={'context': person_data})


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
