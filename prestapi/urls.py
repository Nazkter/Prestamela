from django.conf.urls import url, include
from prestapi import views


urlpatterns = [
    url(r'^$', views.show_form, name='show_form'),
    url(r'^ajax_get_score/$', views.ajax_get_score, name='ajax_get_score'),
    url(r'^ajax_check_email_code/$', views.ajax_check_email_code, name='ajax_check_email_code'),
    url(r'^ajax_create_credit_user/$', views.ajax_create_credit_user, name='ajax_create_credit_user'),
    url(r'^ajax_get_status/$', views.ajax_get_status, name='ajax_get_status'),
    ]
