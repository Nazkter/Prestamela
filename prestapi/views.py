from django.shortcuts import render
from django.http import JsonResponse
from prestapi.models import Config, Client
from prestapi.models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core import mail
import json
import random
import string
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


def ajax_create_credit_user(request):
    email = request.POST.get('email', '')
    if CreditUser.objects.filter(email = email).exists():
        credit_user = CreditUser.objects.get(email = email)
        # it generates a new key for the verification code
        #key = nz_generate_key(email)
        # set the variables for the confirmation email
        #config      = Config.objects.get(pk = 1)
        #subject     = 'Codigo de confirmación para solicitud de credito'
        #mail_to = [email]
        # set the email template variable
        #params = {'key': key}
        #nz_send_mail(config, subject, mail_to, params, 'email_verification_code.html')
        months = request.POST.get('months', '')
        pay_day = request.POST.get('pay_day', '')
        price = request.POST.get('price', '')
        order = request.POST.get('order', '')
        new_credit_request = Request(user=credit_user, order=order, price=price, months=months, pay_day=pay_day)
        try:
            new_credit_request.save()
            response = {"status": True, "response": "Usuario creado correctamente"}
            return JsonResponse(response)
        except:
            response = {"status": False, "response": "No se puede crear la petición."}
            return JsonResponse(response)
        response = {"status": True, "response": "user exists"}
        return JsonResponse(response)
    else:
        new_user = CreditUser(email = email)
        new_user.document_type = request.POST.get('document_type', '')
        new_user.document_id = request.POST.get('document_id', '')
        new_user.first_name = request.POST.get('first_name', '')
        new_user.second_name = request.POST.get('second_name', '')
        new_user.last_name = request.POST.get('last_name', '')
        new_user.second_last_name = request.POST.get('second_last_name', '')
        new_user.expedition_date = request.POST.get('expedition_date', '')
        new_user.birthdate = request.POST.get('birthdate', '')
        new_user.gender = request.POST.get('gender', '')
        new_user.phone = request.POST.get('phone', '')
        new_user.civil_status = request.POST.get('civil_status', '')
        new_user.address_residence = request.POST.get('address_residence', '')
        new_user.type_of_property = request.POST.get('type_of_property', '')
        new_user.work_activity = request.POST.get('work_activity', '')
        new_user.work_type = request.POST.get('work_type', '')
        new_user.personal_reference_first_name = request.POST.get('personal_reference_first_name', '')
        new_user.personal_reference_second_name = request.POST.get('personal_reference_second_name', '')
        new_user.personal_reference_last_name = request.POST.get('personal_reference_last_name', '')
        new_user.personal_reference_second_last_name = request.POST.get('personal_reference_second_last_name', '')
        new_user.personal_reference_phone = request.POST.get('personal_reference_phone', '')
        new_user.personal_reference_city = request.POST.get('personal_reference_city', '')
        new_user.mensual_outgoings = request.POST.get('mensual_outgoings', '')
        new_user.mensual_incomings = request.POST.get('mensual_incomings', '')
        new_user.favorite_bank = request.POST.get('favorite_bank', '')
        try:
            new_user.save()
        except:
            response = {"status": False, "response": "No se puede guardar el usuario."}
            return JsonResponse(response)

        months = request.POST.get('months', '')
        pay_day = request.POST.get('pay_day', '')
        price = request.POST.get('price', '')
        order = request.POST.get('order', '')
        new_credit_request = Request(user=new_user, order=order, price=price, months=months, pay_day=pay_day)
        try:
            #new_user.credit_requests.add(new_credit_request)
            # it generates a new key for the verification code
            #key = nz_generate_key(email)
            # set the variables for the confirmation email
            #config      = Config.objects.get(pk = 1)
            #subject     = 'Codigo de confirmación para solicitud de credito'
            #mail_to = [email]
            # set the email template variable
            #params = {'key': key}
            #nz_send_mail(config, subject, mail_to, params, 'email_verification_code.html')
            new_credit_request.save()
            response = {"status": True, "response": "Usuario creado correctamente"}
            return JsonResponse(response)
        except:
            response = {"status": False, "response": "No se puede crear la petición."}
            return JsonResponse(response)


def ajax_check_email_code(request):
    email_confirmation_code = request.POST.get('email_confirmation_code', '')
    email = request.POST.get('email', '')
    sms_code = request.POST.get('sms_code', '')
    if CreditUser.objects.filter(email = email).exists():
        user = CreditUser.objects.get(email = email)
        user.sms_code = sms_code
        user.save()
        if user.mail_code == email_confirmation_code:
            response = {"status": True, "response": "Código correcto"}
        else:
            response = {"status": False, "response": "Código incorrecto"}
    else:
        response = {"status": False, "response": "Existe usuario."}
    return JsonResponse(response)

def ajax_get_status(request):
    order = request.POST.get('order', None)
    if Request.objects.filter(order=order).exists():
        credit_request = Request.objects.get(order=order)
        status = credit_request.approved if credit_request.approved != None else 'null'
        date = credit_request.approved_date
        response = {"status": status, "order": order, "date": date, "response": 'Datos actualizados'}
    else:
        response = {"status": False, "response": "No existen datos en la base de datos", "order":order}
    return JsonResponse(response)
def ajax_get_score(request):
    # First it gets the form data
    user_email = 'pruebas@pruebas.com'
    user_password = '1026585454'
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
    phone = request.POST.get('phone', '')
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
    response_url = request.POST.get('response_url', '')
    order = request.POST.get('order', '')
    seniority_in_property = request.POST.get('time_in_property', '')
    seniority_in_work = request.POST.get('time_in_work', '')
    has_car = request.POST.get('vehicle', '')
    earnings = request.POST.get('mensual_incomings', '')
    studies = request.POST.get('education_level', '')

    url_login = 'http://dev.bio.credit/integration/prestame/login'
    biocredit_secret = 'QtTvhI1894V7HhlxcCjurdfzju7tTmqqwlwXgr3z'
    biocredit_id = '28'
    import base64
    cod = '{} {}'.format(biocredit_id, biocredit_secret)
    cod_base64 = base64.b64encode(bytes(cod, 'utf-8'))
    try:
        data_login = {
            'email': user_email,
            'password': user_password,
        }
        headers = {'Authorization': cod_base64}
        r = requests.post(url = url_login, data = data_login, headers = headers)
        if r:
            token_type  = r.json()['token_type']
            access_token= r.json()['access_token']
        else:
            return JsonResponse({"status": False,"response": "Login error",'r':str(r)});
    except:
        raise
    # Then it set the required data for the credit score web service
    url = 'http://dev.bio.credit/integration/prestame/give-a-score'
    # data = {
    #     'user_email': user_email,
    #     'user_password': user_password,
    #     'document_type': document_type,
    #     'document_id': document_id,
    #     'first_name': first_name,
    #     'second_name': second_name,
    #     'last_name': last_name,
    #     'second_last_name': second_last_name,
    #     'expedition_date': expedition_date,
    #     'birthdate': birthdate,
    #     'gender': gender,
    #     'email': email,
    #     'phone': phone,
    #     'civil_status': civil_status,
    #     'address_residence': address_residence,
    #     'type_of_property': type_of_property,
    #     'seniority_in_property': seniority_in_property,
    #     'activity': work_activity,
    #     'work_type': work_type,
    #     'seniority_in_work': seniority_in_work,
    #     'personal_reference_first_name': personal_reference_first_name,
    #     'personal_reference_second_name': personal_reference_second_name,
    #     'personal_reference_last_name': personal_reference_last_name,
    #     'personal_reference_second_last_name': personal_reference_second_last_name,
    #     'personal_reference_phone': personal_reference_phone,
    #     'personal_reference_city' : personal_reference_city,
    #     'has_car': has_car,
    #     'earnings': earnings,
    #     'studies': studies,
    # }
    data = {
        'document_type': 1,
        'document_id': '1026569840',
        'first_name': 'Luis Miguel',
        'second_name': '',
        'last_name': 'Gutierrez Ramirez',
        'second_last_name': '',
        'expedition_date': '2009-12-18',
        'birthdate': '1991-12-11',
        'gender': 'm',
        'email': 'ryuuzakiupldr@gmail.com',
        'phone': 3015917459,
        'civil_status': 'Soltero',
        'address_residence': 'Calle 23 #28a-19 apto 401',
        'type_of_property': 'Familiar',
        'seniority_in_property': 'De 3 a 6 meses',
        'activity': 'Independiente',
        'work_type': 'Prestación de Servicios',
        'seniority_in_work': 'De 1 a 5 años',
        'personal_reference_first_name': 'Andrea',
        'personal_reference_second_name': '',
        'personal_reference_last_name': 'Muñoz',
        'personal_reference_second_last_name': '',
        'personal_reference_phone': 3015917459,
        'personal_reference_city' : 'Bogotá',
        'has_car': 'Si',
        'earnings': '4000000',
        'studies': 'Profesional',
    }
    # it makes the POST petition to the web service
    try:
        headers = {'Authorization': '{} {}'.format(token_type, access_token)}
        r = requests.post(url = url, data = data, headers=headers)
        # se envía el correo con la información de la solicitud
    except:
        raise
    if r:
        score = int(r.json()['score'])
        if   score <  600:
            response = {"status": True, "response": "denied", "order": order}
        elif score >= 600 and score < 750:
            response = {"status": True, "response": "pending", "order": order}
        elif score >=  750:
            response = {"status": True, "response": "approved", "order": order}
        else:
            response = {"status": False, "response": "Server error", "order": order}
        # se notifica a la plataforma el estado del prestamo.
        try:
            r = requests.post(url = response_url, data = response)
            # se envía el correo con la información de la solicitud
        except:
            pass
        return JsonResponse(response)
    else:
        return JsonResponse({"status": False,"response": "score API error",'r':str(r.json())});

def nz_send_mail(config, subject, mail_to, params = {}, mail_template=''):
    # Create a manual connection to set the email user
    connection = mail.get_connection(
        host = config.smtp_server,
        port = config.smtp_port,
        username = config.email_sender,
        password = config.email_password ,
        )
    connection.open()
    mail_from = config.email_sender
    msg_html = render_to_string(mail_template, params)
    email2send  = mail.EmailMessage(subject, msg_html, mail_from, to=mail_to, connection=connection)
    email2send.content_subtype = "html"  # Main content is now text/html
    # Send the email using the custom connection
    email2send.send()
    # Close the connection
    connection.close()

def nz_generate_key(email):
    user = CreditUser.objects.get(email = email)
    key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    user.mail_code = key
    user.save()
    return key
