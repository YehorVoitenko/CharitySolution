from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from CharitySolutionAPI.forms import OrganisationPostForm
from CharitySolutionAPI.models import OrganisationPost


def posts_list(request):
    if request.user.is_authenticated:
        post_data = OrganisationPost.objects.all()[::-1]
        return render(request, 'posts_list.html', context={
            'context': post_data
        })
    else:
        return redirect('/error')


def error(request):
    return render(request, 'error.html')


def login_organisation(request):
    if request.method == 'POST':
        organisation_name = request.POST['organisation_name']
        password = request.POST['password']
        organisation = authenticate(request,
                                    username=organisation_name,
                                    password=password)
        if organisation is not None:
            login(request, organisation)
            return redirect('/get_posts_list')
        else:
            return redirect('/error')
    else:
        return render(request, 'login.html')


def logout_organisation(request):
    logout(request)
    return redirect('/login_organisation')


def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = OrganisationPostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return redirect('/get_posts_list')
        form = OrganisationPostForm()
        return render(request, 'create_post.html', {'form': form})
    else:
        return redirect('/error')


def homepage(request):
    return render(request, 'home_page.html')
