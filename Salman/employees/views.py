from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View
from.models import Employee
from services.models import Service
from.forms import EmployeeAddForm
import json

class EmployeesView(View):
    @method_decorator(require_http_methods(["GET"]))
    def get(self, request, *args, **kwargs):
        existing_employees = Employee.objects.filter(business=request.user).prefetch_related('services')
        
        existing_employees_data = [
            {
                'id': str(emp.pk),
                'first_name': emp.first_name,
                'last_name': emp.last_name,
                'phone_number': emp.phone_number,
                'role': emp.role,
                'services': [{'id': service.id, 'name': service.name} for service in emp.services.all()]
            } for emp in existing_employees
        ]
        
        form = EmployeeAddForm(business=request.user)
        services = Service.objects.filter(business=request.user).values('id', 'name')
        
        return render(request, 'employees/employees.html', {
            'existing_employees': existing_employees_data,
            'form': form,
            'services': list(services)
        })

@require_http_methods(["POST"])
def save_employee(request):
    try:
        employee_data = json.loads(request.POST.get('employee'))
        employee_id = employee_data.get('id')
        
        services = employee_data.pop('services', [])
        
        if employee_id and not str(employee_id).startswith('new-'):
            employee = get_object_or_404(Employee, id=employee_id, business=request.user)
            form = EmployeeAddForm(employee_data, instance=employee, business=request.user)
        else:
            form = EmployeeAddForm(employee_data, business=request.user)

        if form.is_valid():
            employee = form.save(commit=False)
            employee.business = request.user
            employee.save()
            
            service_ids = [int(s) for s in services if s]
            services = Service.objects.filter(id__in=service_ids)
            employee.services.set(services)
            
            return JsonResponse({
                'employee': {
                    'id': str(employee.id),
                    'first_name': employee.first_name,
                    'last_name': employee.last_name,
                    'phone_number': employee.phone_number,
                    'role': employee.role,
                    'services': [{'id': s.id, 'name': s.name} for s in employee.services.all()]
                }
            })
        else:
            return JsonResponse({'error': form.errors}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["DELETE"])
def delete_employee(request):
    try:
        employee_id = request.GET.get('id')
        employee = get_object_or_404(Employee, id=employee_id, business=request.user)
        employee.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
