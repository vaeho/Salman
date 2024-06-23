from django.shortcuts import render, redirect
from .forms import BusinessUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.contrib import messages
from . models import BusinessUser
from bookings.models import Booking
from employees.models import Employee
from customers.models import Customer

def signup_view(request):
    if request.method == 'POST':
        form = BusinessUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user instance
            login(request, user)  # Log the user in after signing up
            messages.success(request, 'Your account has been created successfully!')
            return redirect('index')  # Redirect to the dashboard or another appropriate view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusinessUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') 
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'core/index.html')
    


@login_required
def dashboard_view(request):
    current_user = request.user

    # Fetch data that belongs to the current user only
    total_employees = Employee.objects.filter(business=current_user).count()
    total_bookings = Booking.objects.filter(business=current_user).count()
    total_customers = Customer.objects.filter(business=current_user).count()

    recent_bookings = Booking.objects.filter(business=current_user).order_by('-date')[:5]

    # Example dynamic data for customer insights
    customer_insights = {
        'labels': mark_safe(['Returning', 'New', 'Loyal']),  # List of labels
        'data': mark_safe([50, 30, 20])  # Replace with actual data
    }

    context = {
        'total_salons': 1,  # Assuming 1 salon per user in your case
        'total_employees': total_employees,
        'total_bookings': total_bookings,
        'total_customers': total_customers,
        'recent_bookings': recent_bookings,
        'customer_insights': customer_insights,
    }


    return render(request, 'core/dashboard.html', context)

# def add_employee(request):
#     business = request.user
#     if request.method == 'POST':
#         form = EmployeeAddForm(request.POST, business=business)
#         if form.is_valid():
#             form.save()
#             return redirect('employee_list')
#     else:
#         form = EmployeeAddForm(business=business)
#     return render(request, 'salons/add_employee.html', {'form': form})

# def add_booking(request):
#     business = request.user
#     if request.method == 'POST':
#         form = BookingForm(request.POST, business=business)
#         if form.is_valid():
#             form.save()
#             return redirect('booking_list')
#     else:
#         form = BookingForm(business=business)
#     return render(request, 'salons/add_booking.html', {'form': form})
