from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from CharitySolutionAPI.forms import UsersPostForm
from CharitySolutionAPI.models import UsersPost


def posts_list(request):
    if request.user.is_authenticated:
        post_data = UsersPost.objects.all()[::-1]
        return render(request, 'posts_list.html', context={
            'context': post_data
        })
    else:
        return redirect('/error')


def error(request):
    return render(request, 'error.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            login(request, user)
            return redirect('/get_posts_list')
        else:
            return redirect('/error')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/login_user')


def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = UsersPostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return redirect('/get_posts_list')
        form = UsersPostForm()
        return render(request, 'create_post.html', {'form': form})
    else:
        return redirect('/error')


def homepage(request):
    return render(request, 'home_page.html')