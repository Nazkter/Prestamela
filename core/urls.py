from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('prestapi.urls', namespace='api')),
    url(r'^privacy-policy/$', views.show_privacy_policy, name='show_privacy_policy'),
]
