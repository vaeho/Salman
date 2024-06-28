from django.urls import path
from .views import BookingsView, get_employees, get_service_prices

urlpatterns = [
    path('', BookingsView.as_view(), name='bookings'),
    path('get-employees/', get_employees, name='get_employees'),
    path('get-service-prices/', get_service_prices, name='get_service_prices'),
]