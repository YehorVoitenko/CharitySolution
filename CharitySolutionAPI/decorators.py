from CharitySolutionAPI.utils import handler403


def is_user_authenticated(func: object) -> object:
    def wrapper(self, request):
        if request.user.is_authenticated:
            return func(self, request)
        else:
            return handler403(request)

    return wrapper


def is_user_authenticated_with_post_id_param(func: object) -> object:
    def wrapper(self, request, post_id):
        if request.user.is_authenticated:
            return func(self, request, post_id)
        else:
            return handler403(request)

    return wrapper


def is_user_authenticated_with_organisation_id_param(func: object) -> object:
    def wrapper(self, request, organisation_id):
        if request.user.is_authenticated and organisation_id == request.user.id:
            return func(self, request, organisation_id)
        else:
            return handler403(request)

    return wrapper
