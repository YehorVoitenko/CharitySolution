from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from CharitySolutionAPI import views

urlpatterns = [
    path('get_posts_list/', views.posts_list),
    path('error/', views.error),
    path('login_user/', views.login_user),
    path('logout_user/', views.logout_user),
    path('create_post/', views.create_post),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

