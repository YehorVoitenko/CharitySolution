from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as Auth_user
from django.db import IntegrityError

from CharitySolutionAPI.decorators import (
    is_user_authenticated,
    is_user_authenticated_with_post_id_param,
    is_user_authenticated_with_organisation_id_param,
)
from CharitySolutionAPI.forms import OrganisationPostForm, OrganisationForm, UserForm
from CharitySolutionAPI.models import OrganisationPost, Organisation


# JUST RENDERING OR REDIRECTING PAGES
def get_error(request):
    return render(request, "error_pages/error.html")


def get_homepage(request):
    return render(request, "homepage.html")


# RESPONSE DATA FROM DB
def get_posts_list(request):
    # Get all data from OrganisationPost, by inverted 'id'
    post_data = OrganisationPost.objects.all().order_by("-id")
    return render(request, "posts/posts_list.html", context={"context": post_data})


def get_more_info_about_post(request, post_id):
    # Get one post from OrganisationPost, by added post id
    post = OrganisationPost.objects.get(id=post_id)
    organisation = Organisation.objects.get(client_id=post.organisation.client_id)
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
        return render(request, "auth/login_organisation.html")


def logout_current_client(request):
    logout(request)
    return redirect("/")


# POSTS: CREATING, DELETING, EDITING
@is_user_authenticated
def create_post(request):
    if request.method == "POST":
        form = OrganisationPostForm(request.POST, request.FILES)
        organisation = Organisation.objects.get(client_id=request.user.id)
        if form.is_valid():
            temp_object = form.save(commit=False)
            temp_object.organisation = organisation
            temp_object.save()
        return redirect("/get_posts_list")
    form = OrganisationPostForm()
    return render(request, "posts/create_post.html", {"form": form})


@is_user_authenticated_with_post_id_param
def edit_organisation_post(request, post_id):
    post = OrganisationPost.objects.get(id=post_id)

    if request.method == "POST":
        if request.user.id == post.organisation.client_id:
            instance = OrganisationPost.objects.get(id=post_id)
            form = OrganisationPostForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                temp_object = form.save(commit=False)
                temp_object.date_updated = datetime.now()
                temp_object.save()
                return redirect("/get_posts_list")
        else:
            return redirect("/error")

    form = OrganisationPostForm(
        initial={
            "post_text": post.post_text,
            "post_title": post.post_title,
            "help_category": post.help_category,
            "city": post.city,
            "meeting_time": post.meeting_time,
            "meeting_date": post.meeting_date,
        }
    )

    return render(
        request, "posts/edit_organisation_post.html", {"form": form, "post": post}
    )


# @is_user_authenticated_with_post_id_param
def delete_organisation_post(request, post_id):
    post = OrganisationPost.objects.get(id=post_id)
    if request.user.id == post.organisation.client_id:
        OrganisationPost.objects.get(id=post_id).delete()
        return redirect("/get_posts_list")


# ORGANISATIONS CREATING, DELETING, EDITING
@is_user_authenticated_with_organisation_id_param
def edit_organisation_account(request, organisation_id):
    organisation_info = Organisation.objects.get(client_id=organisation_id)

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
        "organisation_site_url": organisation_info.organisation_site_url
    }
    form = OrganisationForm(initial=initial)

    return render(
        request,
        "organisation_account/edit_organisation_account.html",
        {"form": form, "organisation_info": organisation_info},
    )


@is_user_authenticated
def get_organisation_account_view(request):
    organisation = Organisation.objects.get(client_id=request.user.id)
    organisation_posts = OrganisationPost.objects.filter(
        organisation=organisation.id
    ).order_by("-date_created")
    return render(
        request,
        "organisation_account/organisation_account_view.html",
        {"organisation": organisation, "organisation_posts": organisation_posts},
    )


def create_organisation_account(request):
    if request.method == "POST":
        try:
            organisation_name = request.POST["organisation_name"]
            password = request.POST["password"]
            client = Auth_user(username=organisation_name)
            client.set_password(password)
            client.is_superuser = True
            client.is_staff = True
            client.save()
            Organisation.objects.create(
                organisation_name=organisation_name, client_id=client.id
            ).save()
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
            client = Auth_user(username=phone_number)
            client.set_password(password)
            client.save()
            temp_object = form.save(commit=False)
            temp_object.client = client.id
            temp_object.save()
            login(
                request,
                authenticate(request, username=phone_number, password=password),
            )
        return redirect("/get_posts_list")
    form = UserForm()
    return render(request, "user/create_user_account.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        client = authenticate(
            request,
            username=request.POST["phone_number"],
            password=request.POST["password"],
        )
        if client is not None:
            login(request, client)
            return redirect("/get_posts_list")
        else:
            return redirect("/error")
    else:
        return render(request, "user/login_user.html")
