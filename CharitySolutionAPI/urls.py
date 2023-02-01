from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from CharitySolutionAPI import views

urlpatterns = [
    path('get_posts_list/', views.posts_list, name='get_posts_list'),
    path('error/', views.error, name='error'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('create_post/', views.create_post, name='create_post'),
    path('', views.homepage, name='homepage')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

