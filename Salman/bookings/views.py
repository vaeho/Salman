from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .forms import BookingForm
from .models import Booking
from employees.models import Employee
from services.models import Service
from customers.models import Customer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
import json

class BookingsView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = BookingForm(business=request.user)
        view = request.GET.get('view', 'week')
        start_date = request.GET.get('start_date')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            start_date = datetime.now().date()

        if view == 'day':
            end_date = start_date
        elif view == 'month':
            next_month = start_date.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
        else:
            end_date = start_date + timedelta(days=6)

        bookings = Booking.objects.filter(
            business=request.user,
            date__range=[start_date, end_date]
        ).select_related('service', 'employee', 'customer')
        
        # Serialize bookings to JSON
        json_bookings = json.dumps(list(bookings.values('date', 'time', 'service__name', 'customer__first_name', 'customer__last_name')), cls=DjangoJSONEncoder)

        return render(request, 'bookings/bookings.html', {
            'form': form,
            'bookings': bookings,
            'json_bookings': json_bookings,  # Pass JSON to context
            'start_date': start_date,
            'view': view
        })

    @method_decorator(login_required)
    def post(self, request):
        form = BookingForm(request.POST, business=request.user)
        if form.is_valid():
            try:
                with transaction.atomic():
                    customer, created = Customer.objects.update_or_create(
                        phone_number=form.cleaned_data['customer_phone_number'],
                        defaults={
                            'first_name': form.cleaned_data['customer_first_name'],
                            'last_name': form.cleaned_data['customer_last_name'],
                            'email': form.cleaned_data['customer_email'],
                            'business': request.user,
                        }
                    )

                    services = form.cleaned_data['services']
                    for service in services:
                        booking = Booking.objects.create(
                            business=request.user,
                            service=service,
                            employee=form.cleaned_data['employee'],
                            customer=customer,
                            date=form.cleaned_data['date'],
                            time=form.cleaned_data['time'],
                            total_amount=form.cleaned_data['total_amount'] / len(services)  # Divide total amount among services
                        )

                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'errors': str(e)}, status=500)
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

def get_employees(request):
    service_ids = request.GET.getlist('service_ids[]')
    employees = Employee.objects.filter(services__id__in=service_ids, business=request.user).distinct()
    return JsonResponse(list(employees.values('id', 'first_name', 'last_name')), safe=False)

def get_service_prices(request):
    service_ids = request.GET.getlist('service_ids[]')
    services = Service.objects.filter(id__in=service_ids, business=request.user)
    return JsonResponse({str(service.id): str(service.price) for service in services})
