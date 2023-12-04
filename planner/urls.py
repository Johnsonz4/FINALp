from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import path,reverse,reverse_lazy, re_path

app_name = "planner"

urlpatterns = [
    path('', views.index, name="index"),
    path('create_travel_plan', views.create_travel_plan, name="create_travel_plan"),
    path('add_travel_plan_item', views.add_travel_plan_item, name="add_travel_plan_item"),
    path('delete_travel_plan_item', views.delete_travel_plan_item, name="delete_travel_plan_item"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('travel_plan/<str:id>/', views.travel_plan, name = "travel_plan"),
    path('register', views.register, name="register"),
    path('login_user', views.login_user, name="login_user"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('profile', views.profile, name="profile"),
]
