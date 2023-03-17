from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from CharitySolutionAPI import views

urlpatterns = [
    path(
        "edit_organisation_post/<int:post_id>",
        views.EditOrganisationPost.as_view(),
        name="edit_organisation_post",
    ),
    path(
        "get_more_info_about_post/<int:post_id>",
        views.PostInfo.as_view(),
        name="get_more_info_about_post",
    ),
    path(
        "delete_organisation_post/<int:post_id>",
        views.DeleteOrganisationPost.as_view(),
        name="delete_organisation_post",
    ),
    path(
        "edit_organisation_account/<int:organisation_id>",
        views.EditOrganisationAccount.as_view(),
        name="edit_organisation_account",
    ),
    # Login/Logout URLs
    path(
        "login_organisation/",
        views.LoginOrganisation.as_view(),
        name="login_organisation",
    ),
    path(
        "logout_current_client/",
        views.LogOut.as_view(),
        name="logout_current_client",
    ),
    path("login_user/", views.LoginUser.as_view(), name="login_user"),
    path("create_post/", views.CreatePost.as_view(), name="create_post"),
    path(
        "create_organisation_account/",
        views.CreateOrganisationAccount.as_view(),
        name="create_organisation_account",
    ),
    path(
        "create_user_account/",
        views.CreateUserAccount.as_view(),
        name="create_user_account",
    ),
    path("get_post_roll/", views.PostRoll.as_view(), name="get_post_roll"),
    path(
        "organisation_bio/<int:organisation_id>",
        views.OrganisationBio.as_view(),
        name="get_organisation_bio",
    ),
    path(
        "get_organisation_account_view/",
        views.OrganisationAccountView.as_view(),
        name="get_organisation_account_view",
    ),
    path(
        "registrate_for_help/<int:post_id>/",
        views.RegistrateNeedy.as_view(),
        name="registrate_for_help",
    ),
    path(
        "registration_info_for_organisation/<int:post_id>",
        views.RegistrationInfoForOrganisation.as_view(),
        name="registration_info_for_organisation",
    ),
    path("", views.Homepage.as_view(), name="homepage"),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
