from django.urls import path, include

from CharitySolutionAPI import views

urlpatterns = [
    path('get_users_list/', views.user_list),
    path('registration/save_user_info/', views.save_user_info),
    path('registration/', views.registration),
    path('error/', views.error),
    path('login_member/', views.login_user),
    path('logout_member/', views.logout_user),
]
