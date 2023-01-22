from django.contrib import admin
from django.urls import path

from CharitySolutionAPI import views

urlpatterns = [
    path('', views.homepage),
]
