from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as Auth_user
from django.db import IntegrityError

from CharitySolutionAPI.decorators import (
    is_user_authenticated,
    is_user_authenticated_with_post_id_param,
    is_user_authenticated_with_organisation_id_param,
)
from CharitySolutionAPI.forms import (
    OrganisationPostForm,
    OrganisationForm,
    UserForm,
)
from CharitySolutionAPI.models import OrganisationPost, Organisation
from CharitySolutionAPI.utils import handler401, handler400, handler403


def get_homepage(request):
    return render(request, "common_pages/homepage.html")


# RESPONSE DATA FROM DB
def get_posts_list(request):
    return render(
        request,
        "posts/posts_list.html",
        context={
            "context": OrganisationPost.objects.all()
            .order_by("-id")
            .select_related("organisation")
        },
    )


def get_organisation_bio(request, organisation_id):
    return render(
        request,
        "common_pages/organisation_bio.html",
        {
            "organisation": get_object_or_404(Organisation, pk=organisation_id),
            "organisation_post": OrganisationPost.objects.filter(
                organisation_id=organisation_id
            ),
        },
    )


def get_more_info_about_post(request, post_id):
    return render(
        request,
        "posts/get_more_info_about_post.html",
        {
            "organisation_and_posts": get_object_or_404(
                OrganisationPost.objects.select_related("organisation"), pk=post_id
            )
        },
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
            return handler401(request)

    return render(request, "auth/login_organisation.html")


def logout_current_client(request):
    logout(request)
    return redirect("/")


# POSTS: CREATING, DELETING, EDITING
@is_user_authenticated
def create_post(request):
    if request.method == "POST":
        form = OrganisationPostForm(request.POST, request.FILES)
        if form.is_valid():
            temp_object = form.save(commit=False)
            temp_object.organisation = Organisation.objects.get(
                client_id=request.user.id
            )
            temp_object.save()
        return redirect("/get_posts_list")
    form = OrganisationPostForm()
    return render(request, "posts/create_post.html", {"form": form})


@is_user_authenticated_with_post_id_param
def edit_organisation_post(request, post_id):
    post = get_object_or_404(OrganisationPost, pk=post_id)

    if request.method == "POST":
        if request.user.id == post.organisation.client_id.id:
            instance = OrganisationPost.objects.get(id=post_id)
            form = OrganisationPostForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                temp_object = form.save(commit=False)
                temp_object.date_updated = datetime.now()
                temp_object.save()
                return redirect("/get_posts_list")
        else:
            return handler403(request)

    form = OrganisationPostForm(
        initial={
            "post_text": post.post_text,
            "post_title": post.post_title,
            "help_category": post.help_category,
            "city": post.city,
        }
    )

    return render(
        request, "posts/edit_organisation_post.html", {"form": form, "post": post}
    )


@is_user_authenticated_with_post_id_param
def delete_organisation_post(request, post_id):
    post = get_object_or_404(OrganisationPost, pk=post_id)

    if request.user.id == post.organisation.client_id.id:
        OrganisationPost.objects.get(id=post_id).delete()
        return redirect("/get_posts_list")


# ORGANISATIONS CREATING, DELETING, EDITING
@is_user_authenticated_with_organisation_id_param
def edit_organisation_account(request, organisation_id):
    organisation_info = get_object_or_404(Organisation, client_id=organisation_id)

    if request.method == "POST":
        form = OrganisationForm(request.POST, request.FILES, instance=organisation_info)
        if form.is_valid():
            form.save()
            return redirect("/get_organisation_account_view")

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
def get_organisation_account_view(request):
    organisation = get_object_or_404(Organisation, client_id=request.user.id)

    return render(
        request,
        "organisation_account/organisation_account_view.html",
        {
            "organisation": organisation,
            "organisation_posts": OrganisationPost.objects.filter(
                organisation=organisation.id
            ).order_by("-date_created"),
        },
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
                organisation_name=organisation_name, client_id=client
            ).save()
            login(
                request,
                authenticate(request, username=organisation_name, password=password),
            )
            return redirect("/get_posts_list")
        except IntegrityError:
            return handler401(request)

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
            temp_object.client_id = client
            temp_object.save()
            login(
                request,
                authenticate(request, username=phone_number, password=password),
            )
        else:
            return handler400(request)
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
            return handler401(request)
    else:
        return render(request, "user/login_user.html")
