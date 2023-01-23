from django.urls import path

from CharitySolutionAPI import views

urlpatterns = [
    path('', views.homepage),
    path('registration/get_user_info/', views.save_user_info),
    path('registration/', views.registration),
]
