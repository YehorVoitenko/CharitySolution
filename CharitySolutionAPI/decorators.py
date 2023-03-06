from django.shortcuts import redirect


def is_user_authenticated(func):
    def wrapper(request):
        if request.user.is_authenticated:
            return func(request)
        else:
            return redirect("/error")

    return wrapper


def is_user_authenticated_with_post_id_param(func):
    def wrapper(request, post_id):
        if request.user.is_authenticated:
            return func(request, post_id)
        else:
            return redirect("/error")

    return wrapper


def is_user_authenticated_with_organisation_id_param(func):
    def wrapper(request, organisation_id):
        if request.user.is_authenticated and organisation_id == request.user.id:
            return func(request, organisation_id)
        else:
            return redirect("/error")

    return wrapper
