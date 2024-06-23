from django.urls import path
from. import views

urlpatterns = [
    path('', views.EmployeesView.as_view(), name='employees'),
    path('save-employee/', views.save_employee, name='save_employee'),
    path('delete-employee/', views.delete_employee, name='delete_employee'),
]
