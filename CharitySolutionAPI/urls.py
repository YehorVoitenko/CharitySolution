from django.urls import path, include

from CharitySolutionAPI import views

urlpatterns = [
    path('get_items_list/', views.items_list),
    path('save_item_info/', views.save_item_info),
    path('add_item/', views.add_item),
    path('error/', views.error),
    path('login_user/', views.login_user),
    path('logout_user/', views.logout_user),
]
