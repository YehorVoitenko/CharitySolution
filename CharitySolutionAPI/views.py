from django.shortcuts import render

from CharitySolutionAPI.models import Person


def homepage(request):
    tom = Person(name="Test", age=23)
    tom.save()
    saved_tom = Person.objects.all()
    return render(request, 'index.html', context={'context': saved_tom})
