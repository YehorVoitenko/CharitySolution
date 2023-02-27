from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

from CharitySolutionAPI.forms import OrganisationPostForm, OrganisationForm
from CharitySolutionAPI.models import OrganisationPost, Organisation


# JUST RENDERING OR REDIRECTING PAGES
def error(request):
    return render(request, 'error_pages/error.html')

def homepage(request):
    return render(request, 'homepage.html')


# RESPONSE DATA FROM DB
def posts_list(request):
    # Get all data from OrganisationPost, by inverted 'id'
    post_data = OrganisationPost.objects.all().order_by('-id')
    return render(request, 'posts/posts_list.html', context={'context': post_data})


def get_more_info_about_post(request, post_id):
    # Get one post from OrganisationPost, by added post id
    post = OrganisationPost.objects.get(id=post_id)
    return render(request, 'posts/get_more_info_about_post.html', {'post': post})


# AUTH VIEWS
def login_organisation(request):
    if request.method == 'POST':
        organisation = authenticate(
            request,
            username=request.POST['organisation_name'],
            password=request.POST['password']
        )
        if organisation is not None:
            login(request, organisation)
            return redirect('/get_posts_list')
        else:
            return redirect('/error')
    else:
        return render(request, 'auth/login.html')


def logout_organisation(request):
    logout(request)
    return redirect('/login_organisation')


# POSTS CREATING, DELETING, EDITING
def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = OrganisationPostForm(request.POST, request.FILES)
            organisation = Organisation.objects.get(pk=request.user.id)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.organisation = organisation
                obj.save()
            return redirect('/get_posts_list')
        form = OrganisationPostForm()
        return render(request, 'posts/create_post.html', {'form': form})
    else:
        return redirect('/error')


def edit_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            instance = OrganisationPost.objects.get(id=post_id)
            form = OrganisationPostForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.date_updated = datetime.now()
                obj.save()
                return redirect('/get_posts_list')
        post = OrganisationPost.objects.get(id=post_id)

        form = OrganisationPostForm(initial={'post_text': post.post_text, 'post_title': post.post_title})

        return render(request, 'posts/edit_post.html', {'form': form, 'post': post})
    else:
        return redirect('/error')


def delete_post(request, post_id):
    if request.user.is_authenticated:
        post = OrganisationPost.objects.get(id=post_id)
        if post.organisation_id == request.user.id:
            OrganisationPost.objects.get(id=post_id).delete()
            return redirect('/get_posts_list')
    else:
        return redirect('/error')


# ORGANISATIONS CREATING, DELETING, EDITING
def edit_organisation_account(request, organisation_id):
    if request.user.is_authenticated and organisation_id == request.user.id:
        organisation_info = Organisation.objects.get(id=organisation_id)

        if request.method == "POST":
            form = OrganisationForm(request.POST, request.FILES, instance=organisation_info)
            if form.is_valid():
                form.save()
                return redirect('/account')

        initial = {
            'organisation_name': organisation_info.organisation_name,
            'organisation_description': organisation_info.organisation_description,
            'city': organisation_info.city,
            'email': organisation_info.email,
            'telegram_nick': organisation_info.telegram_nick,
            'instagram_nick': organisation_info.instagram_nick,
            'organisation_site_url': organisation_info.organisation_site_url,
        }
        form = OrganisationForm(initial=initial)

        return render(request, 'organisation_account/edit_organisation_account.html', {
            'form': form,
            'organisation_info': organisation_info
        }
                      )
    else:
        return redirect('/error')


def get_account_view(request):
    if request.user.is_authenticated:
        organisation = Organisation.objects.get(pk=request.user.id)
        organisation_posts = OrganisationPost.objects.filter(organisation=request.user.id).order_by('-date_created')
        return render(request, 'organisation_account/account_view.html', {'organisation': organisation,
                                                                          'organisation_posts': organisation_posts})
    else:
        return redirect('/error')


def create_organisation(request):
    if request.method == "POST":
        try:
            organisation_name = request.POST['organisation_name']
            password = request.POST['password']
            u = User(username=organisation_name)
            Organisation.objects.create(organisation_name=organisation_name).save()
            u.set_password(password)
            u.is_superuser = True
            u.is_staff = True
            u.save()
            login(request, authenticate(request, username=organisation_name, password=password))
            return redirect('/get_posts_list')
        except IntegrityError:
            return HttpResponse("<div align='center'><h1>Sorry, this organisation is already exists</h1></div>")

    return render(request, 'organisation_account/create_organisation.html')

