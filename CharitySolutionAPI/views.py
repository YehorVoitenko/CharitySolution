from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as Auth_user
from django.db import IntegrityError
from django.views import View

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


class Homepage(View):
    def get(self, request):
        return render(request, "common_pages/homepage.html")


class PostRoll(View):
    def get(self, request):
        return render(
            request,
            "posts/posts_list.html",
            context={
                "context": OrganisationPost.objects.all()
                .order_by("-id")
                .select_related("organisation")
            },
        )

    def post(self, request):
        ...


class OrganisationBio(View):
    def get(self, request, organisation_id):
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


class PostInfo(View):
    def get(self, request, post_id):
        return render(
            request,
            "posts/get_more_info_about_post.html",
            {
                "organisation_and_posts": get_object_or_404(
                    OrganisationPost.objects.select_related("organisation"), pk=post_id
                )
            },
        )


class LoginOrganisation(View):
    def get(self, request):
        return render(request, "auth/login_organisation.html")

    def post(self, request):
        if request.method == "POST":
            organisation = authenticate(
                request,
                username=request.POST["organisation_name"],
                password=request.POST["password"],
            )
            if organisation is not None:
                login(request, organisation)
                return redirect("/get_post_roll")
            else:
                return handler401(request)


class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class CreatePost(View):
    @is_user_authenticated
    def get(self, request):
        form = OrganisationPostForm()
        return render(request, "posts/create_post.html", {"form": form})

    def post(self, request):
        form = OrganisationPostForm(request.POST, request.FILES)
        if form.is_valid():
            temp_object = form.save(commit=False)
            temp_object.organisation = Organisation.objects.get(
                client_id=request.user.id
            )
            temp_object.save()
        return redirect("/get_post_roll")


class EditOrganisationPost(View):
    @is_user_authenticated_with_post_id_param
    def get(self, request, post_id):
        post = get_object_or_404(OrganisationPost, pk=post_id)
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

    def post(self, request, post_id):
        post = get_object_or_404(OrganisationPost, pk=post_id)
        if request.method == "POST":
            if request.user.id == post.organisation.client_id.id:
                instance = OrganisationPost.objects.get(id=post_id)
                form = OrganisationPostForm(
                    request.POST, request.FILES, instance=instance
                )
                if form.is_valid():
                    temp_object = form.save(commit=False)
                    temp_object.date_updated = datetime.now()
                    temp_object.save()
                    return redirect("/get_post_roll")
            else:
                return handler403(request)


class DeleteOrganisationPost(View):
    @is_user_authenticated_with_post_id_param
    def get(self, request, post_id):
        post = get_object_or_404(OrganisationPost, pk=post_id)

        if request.user.id == post.organisation.client_id.id:
            OrganisationPost.objects.get(id=post_id).delete()
            return redirect("/get_post_roll")


class EditOrganisationAccount(View):
    @is_user_authenticated_with_organisation_id_param
    def get(self, request, organisation_id):
        organisation_info = get_object_or_404(Organisation, client_id=organisation_id)
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

    def post(self, request, organisation_id):
        organisation_info = get_object_or_404(Organisation, client_id=organisation_id)
        if request.method == "POST":
            form = OrganisationForm(
                request.POST, request.FILES, instance=organisation_info
            )
            if form.is_valid():
                form.save()
                return redirect("/get_organisation_account_view")


class OrganisationAccountView(View):
    @is_user_authenticated
    def get(self, request):
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


class CreateOrganisationAccount(View):
    def get(
        self,
        request,
    ):
        return render(request, "organisation_account/create_organisation.html")

    def post(self, request):
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
            return redirect("/get_post_roll")
        except IntegrityError:
            return handler401(request)


class CreateUserAccount(View):
    def get(self, request):
        return render(request, "user/create_user_account.html", {"form": UserForm()})

    def post(self, request):
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
        return redirect("/get_post_roll")


class LoginUser(View):
    def get(self, request):
        return render(request, "user/login_user.html")

    def post(self, request):
        client = authenticate(
            request,
            username=request.POST["phone_number"],
            password=request.POST["password"],
        )
        if client is not None:
            login(request, client)
            return redirect("/get_post_roll")
        else:
            return handler401(request)
