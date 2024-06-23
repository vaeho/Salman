# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Service
from .forms import ServiceForm
from django.core.serializers import serialize
import json

@require_http_methods(["GET"])
def services_view(request):
    existing_services = Service.objects.filter(business=request.user)
    existing_services_json = serialize('json', existing_services)
    form = ServiceForm()
    return render(request, 'services/services.html', {
        'existing_services': json.loads(existing_services_json),
        'form': form
    })


@require_http_methods(["POST"])
def save_service(request):
    try:
        service_data = json.loads(request.POST.get('service'))
        service_id = service_data.get('id')
        
        if service_id and not service_id.startswith('new-'):
            service = get_object_or_404(Service, id=service_id, business=request.user)
            form = ServiceForm(service_data, instance=service)
        else:
            form = ServiceForm(service_data)

        if form.is_valid():
            service = form.save(commit=False)
            service.business = request.user
            service.save()
            return JsonResponse({
                'service': {
                    'id': str(service.id),
                    'name': service.name,
                    'description': service.description,
                    'price': str(service.price),
                    'duration': service.duration
                }
            })
        else:
            return JsonResponse({'error': form.errors}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["DELETE"])
def delete_service(request):
    try:
        service_id = request.GET.get('id')
        service = get_object_or_404(Service, id=service_id, business=request.user)
        service.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)