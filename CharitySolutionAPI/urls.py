from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from CharitySolutionAPI import views

urlpatterns = [
    # URLs with parameters
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
    path('get_more_info_about_post/<int:post_id>', views.get_more_info_about_post,
         name='get_more_info_about_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('edit_organisation_account/<int:organisation_id>', views.edit_organisation_account,
         name='edit_organisation_account'),

    # Login/Logout URLs
    path('login_organisation/', views.login_organisation, name='login_organisation'),
    path('logout_organisation/', views.logout_organisation, name='logout_organisation'),

    # Creating URLs
    path('create_post/', views.create_post, name='create_post'),
    path('create_organisation/', views.create_organisation, name='create_organisation'),

    # Getting info URLs
    path('get_posts_list/', views.posts_list, name='get_posts_list'),
    path('get_account_view/', views.get_account_view, name='get_account_view'),
    path('error/', views.error, name='error'),

    # Homepage URL
    path('', views.homepage, name='homepage'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
