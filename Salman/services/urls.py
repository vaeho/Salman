from django.urls import path
from . import views

urlpatterns = [
    path('', views.services_view, name='services'),
    path('save-service/', views.save_service, name='save_service'),
    path('delete-service/', views.delete_service, name='delete_service'),
]