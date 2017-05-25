from django.shortcuts import render
from django.http import JsonResponse
from prestapi.models import Config, Client
import json
import requests



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


def ajax_get_score(request):
    # First it gets the form data
    user_email = request.POST.get('user_email', '')
    user_password = request.POST.get('user_password', '')
    document_type = request.POST.get('document_type', '')
    document_id = request.POST.get('document_id', '')
    first_name = request.POST.get('first_name', '')
    second_name = request.POST.get('second_name', '')
    last_name = request.POST.get('last_name', '')
    second_last_name = request.POST.get('second_last_name', '')
    expedition_date = request.POST.get('expedition_date', '')
    birthdate = request.POST.get('birthdate', '')
    gender = request.POST.get('gender', '')
    email = request.POST.get('email', '')
    phone = int(request.POST.get('phone', ''))
    civil_status = request.POST.get('civil_status', '')
    address_residence = request.POST.get('address_residence', '')
    type_of_property = request.POST.get('type_of_property', '')
    work_activity = request.POST.get('work_activity', '')
    work_type = request.POST.get('work_type', '')
    personal_reference_first_name = request.POST.get('personal_reference_first_name', '')
    personal_reference_second_name = request.POST.get('personal_reference_second_name', '')
    personal_reference_last_name = request.POST.get('personal_reference_last_name', '')
    personal_reference_second_last_name = request.POST.get('personal_reference_second_last_name', '')
    personal_reference_phone = request.POST.get('personal_reference_phone', '')
    personal_reference_city = request.POST.get('personal_reference_city', '')

    # Then it set the required data for the credit score web service
    url = 'http://dev.bio.credit/integration/prestame/give-a-score'
    data = {
        'user_email': user_email,
        'user_password': user_password,
        'document_type': document_type,
        'document_id': document_id,
        'first_name': first_name,
        'second_name': second_name,
        'last_name': last_name,
        'second_last_name': second_last_name,
        'expedition_date': expedition_date,
        'birthdate': birthdate,
        'gender': gender,
        'email': email,
        'phone': phone,
        'civil_status': civil_status,
        'address_residence': address_residence,
        'type_of_property': type_of_property,
        'work_activity': work_activity,
        'work_type': work_type,
        'personal_reference_first_name': personal_reference_first_name,
        'personal_reference_second_name': personal_reference_second_name,
        'personal_reference_last_name': personal_reference_last_name,
        'personal_reference_second_last_name': personal_reference_second_last_name,
        'personal_reference_phone': personal_reference_phone,
        'personal_reference_city' : personal_reference_city,
    }
    # it makes the POST petition to the web service
    try:
        r = requests.post(url = url, data = data)
    except:
        raise
    print(r)
    return JsonResponse(r.json());
