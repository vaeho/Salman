from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='account_login'),
    path('signup/', views.signup_view, name='account_signup'),
    path('logout/', views.logout_view, name='account_logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
