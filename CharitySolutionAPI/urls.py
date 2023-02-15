from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from CharitySolutionAPI import views

urlpatterns = [
    path('get_posts_list/', views.posts_list, name='get_posts_list'),
    path('account/', views.account, name='account'),
    path('error/', views.error, name='error'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('login_organisation/', views.login_organisation, name='login_organisation'),
    path('logout_organisation/', views.logout_organisation, name='logout_organisation'),
    path('create_post/', views.create_post, name='create_post'),
    path('create_organisation/', views.create_organisation, name='create_organisation'),
    path('edit_organisation_account/<int:organisation_id>', views.edit_organisation_account,
         name='edit_organisation_account'),
    path('', views.homepage, name='homepage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
