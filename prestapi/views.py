from django.shortcuts import render
from django.http import JsonResponse
from prestapi.models import Config, Client
import json


def show_privacy_policy(request):
    return render(request, 'privacy-policy.html')
# Create your views here.
def show_form(request):
    # 1 - Obtengo las credenciales y las cotejo con BD
    # 2 - Tomo los datos entrantes y despliego la interfaz
    config = Config.objects.all()[0]
    account_id  = request.GET.get('account_id', None)
    secret_key  = request.GET.get('secret_key', None)
    total       = request.GET.get('products_total', None)
    logo_url    = request.GET.get('logo_url', None)

    if secret_key and account_id:
        if Client.objects.filter(secret_key = secret_key, account_id = account_id).exists():
            context = { 'total':    total,
                        'logo_url': logo_url,
                        'config': config,
                      }
            return render(request, 'index.html', context)
        else:
            response  = {   'success': False,
                            'error': True,
                            'msg': 'Cliente no existe',
                        }
    else:
        return render(request, 'home.html')
        '''response  = {   'success': False,
                        'error': True,
                        'msg': 'Datos faltantes',
                    }'''
    return JsonResponse( response )


def get_score(request):
    # 1 - Obtengo las credenciales y las cotejo con BD
    # 2 - Tomo los datos entrantes y despliego la interfaz

    return JsonResponse(
        {
            'success': True,
            'error': False,
            'msg': 'Petición correcta.',
        }
    );
