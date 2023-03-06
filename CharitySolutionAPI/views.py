from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as auth_user
from django.db import IntegrityError

from CharitySolutionAPI.decorators import (
    is_user_authenticated,
    is_user_authenticated_with_post_id_param,
    is_user_authenticated_with_organisation_id_param,
)
from CharitySolutionAPI.forms import OrganisationPostForm, OrganisationForm, UserForm
from CharitySolutionAPI.models import OrganisationPost, Organisation, User as model_user


# JUST RENDERING OR REDIRECTING PAGES
def error(request):
    return render(request, "error_pages/error.html")


def homepage(request):
    return render(request, "homepage.html")


# RESPONSE DATA FROM DB
def posts_list(request):
    # Get all data from OrganisationPost, by inverted 'id'
    post_data = OrganisationPost.objects.all().order_by("-id")
    return render(request, "posts/posts_list.html", context={"context": post_data})


def get_more_info_about_post(request, post_id):
    # Get one post from OrganisationPost, by added post id
    post = OrganisationPost.objects.get(id=post_id)
    organisation = Organisation.objects.get(client_id=request.user.id)
    return render(
        request,
        "posts/get_more_info_about_post.html",
        {"post": post, "organisation": organisation},
    )


# AUTH VIEWS
def login_organisation(request):
    if request.method == "POST":
        organisation = authenticate(
            request,
            username=request.POST["organisation_name"],
            password=request.POST["password"],
        )
        if organisation is not None:
            login(request, organisation)
            return redirect("/get_posts_list")
        else:
            return redirect("/error")
    else:
        return render(request, "auth/login.html")


def logout_organisation(request):
    logout(request)
    return redirect("/login_organisation")


# POSTS: CREATING, DELETING, EDITING
@is_user_authenticated
def create_post(request):
    if request.method == "POST":
        form = OrganisationPostForm(request.POST, request.FILES)
        organisation = Organisation.objects.get(client_id=request.user.id)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.organisation = organisation
            obj.save()
        return redirect("/get_posts_list")
    form = OrganisationPostForm()
    return render(request, "posts/create_post.html", {"form": form})


@is_user_authenticated_with_post_id_param
def edit_post(request, post_id):
    if request.method == "POST":
        instance = OrganisationPost.objects.get(id=post_id)
        form = OrganisationPostForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.date_updated = datetime.now()
            obj.save()
            return redirect("/get_posts_list")
    post = OrganisationPost.objects.get(id=post_id)

    form = OrganisationPostForm(
        initial={
            "post_text": post.post_text,
            "post_title": post.post_title,
            "help_category": post.help_category,
            "city": post.city,
        }
    )

    return render(request, "posts/edit_post.html", {"form": form, "post": post})


@is_user_authenticated_with_post_id_param
def delete_post(request, post_id):
    post = OrganisationPost.objects.get(id=post_id)
    if post.organisation_id == request.user.id:
        OrganisationPost.objects.get(id=post_id).delete()
        return redirect("/get_posts_list")


# ORGANISATIONS CREATING, DELETING, EDITING
@is_user_authenticated_with_organisation_id_param
def edit_organisation_account(request, organisation_id):
    organisation_info = Organisation.objects.get(id=organisation_id)

    if request.method == "POST":
        form = OrganisationForm(request.POST, request.FILES, instance=organisation_info)
        if form.is_valid():
            form.save()
            return redirect("/get_account_view")

    initial = {
        "organisation_name": organisation_info.organisation_name,
        "organisation_description": organisation_info.organisation_description,
        "city": organisation_info.city,
        "email": organisation_info.email,
        "telegram_nick": organisation_info.telegram_nick,
        "instagram_nick": organisation_info.instagram_nick,
        "organisation_site_url": organisation_info.organisation_site_url,
    }
    form = OrganisationForm(initial=initial)

    return render(
        request,
        "organisation_account/edit_organisation_account.html",
        {"form": form, "organisation_info": organisation_info},
    )


@is_user_authenticated
def get_account_view(request):
    organisation = Organisation.objects.get(client_id=request.user.id)
    organisation_posts = OrganisationPost.objects.filter(
        organisation=request.user.id
    ).order_by("-date_created")
    return render(
        request,
        "organisation_account/account_view.html",
        {"organisation": organisation, "organisation_posts": organisation_posts},
    )


def create_organisation(request):
    if request.method == "POST":
        try:
            organisation_name = request.POST["organisation_name"]
            password = request.POST["password"]
            u = auth_user(username=organisation_name)
            u.set_password(password)
            u.is_superuser = True
            u.is_staff = True
            u.save()
            Organisation.objects.create(organisation_name=organisation_name, client_id=u.id).save()
            login(
                request,
                authenticate(request, username=organisation_name, password=password),
            )
            return redirect("/get_posts_list")
        except IntegrityError:
            return HttpResponse(
                "<div align='center'><h1>Sorry, this organisation is already exists</h1></div>"
            )

    return render(request, "organisation_account/create_organisation.html")


# USER VIEWS
def create_user_account(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        phone_number = request.POST["phone_number"]
        password = request.POST["password"]
        if form.is_valid():
            user = auth_user(username=phone_number)
            user.set_password(password)
            user.is_superuser = False
            user.is_staff = False
            user.save()
            client = user.id
            obj = form.save(commit=False)
            obj.client = client
            obj.save()
            login(
                request,
                authenticate(request, username=phone_number, password=password),
            )
        return redirect("/get_posts_list")
    form = UserForm()
    return render(request, "user/create_user_account.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["phone_number"],
            password=request.POST["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("/get_posts_list")
        else:
            return redirect("/error")
    else:
        return render(request, "user/login_user.html")
