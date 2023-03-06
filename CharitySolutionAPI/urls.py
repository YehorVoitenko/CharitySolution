from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from CharitySolutionAPI import views

urlpatterns = [
    # URLs with parameters
    path(
        "edit_organisation_post/<int:post_id>",
        views.edit_organisation_post,
        name="edit_organisation_post",
    ),
    path(
        "get_more_info_about_post/<int:post_id>",
        views.get_more_info_about_post,
        name="get_more_info_about_post",
    ),
    path(
        "delete_organisation_post/<int:post_id>",
        views.delete_organisation_post,
        name="delete_organisation_post",
    ),
    path(
        "edit_organisation_account/<int:organisation_id>",
        views.edit_organisation_account,
        name="edit_organisation_account",
    ),
    # Login/Logout URLs
    path("login_organisation/", views.login_organisation, name="login_organisation"),
    path(
        "logout_current_client/",
        views.logout_current_client,
        name="logout_current_client",
    ),
    path("login_user/", views.login_user, name="login_user"),
    # Creating URLs
    path("create_post/", views.create_post, name="create_post"),
    path(
        "create_organisation_account/",
        views.create_organisation_account,
        name="create_organisation_account",
    ),
    path("create_user_account/", views.create_user_account, name="create_user_account"),
    # Getting info URLs
    path("get_posts_list/", views.get_posts_list, name="get_posts_list"),
    path(
        "get_account_view/",
        views.get_organisation_account_view,
        name="get_account_view",
    ),
    path("error/", views.get_error, name="error"),
    # Homepage URL
    path("", views.get_homepage, name="homepage"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
