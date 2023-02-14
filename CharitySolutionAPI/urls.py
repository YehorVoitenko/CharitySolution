from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from CharitySolutionAPI import views

urlpatterns = [
    path('get_posts_list/', views.posts_list, name='get_posts_list'),
    path('account/', views.account, name='account'),
    path('error/', views.error, name='error'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
    path('login_organisation/', views.login_organisation, name='login_organisation'),
    path('logout_organisation/', views.logout_organisation, name='logout_organisation'),
    path('create_post/', views.create_post, name='create_post'),
    path('', views.homepage, name='homepage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

