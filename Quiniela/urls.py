from django.conf.urls import patterns, include, url
from django.conf import settings
from app import views
from django.contrib import admin
admin.autodiscover()
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', 'Quiniela.views.home', name='home'),
    # url(r'^Quiniela/', include('Quiniela.foo.urls')),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name':'inicio.html'}, name = "login"),
    url(r'^cerrar/$', 'django.contrib.auth.views.logout_then_login', name = "logout"),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^mispartidos/$', 'app.views.mispartidos', name = 'mispartidos'),
    url(r'^administracion/$', 'app.views.administracion', name = 'administracion'),
    url(r'^vertabla/$', 'app.views.vertabla', name = 'vertabla'),
    url(r'^posiciones/$', 'app.views.posiciones', name = 'posiciones'),
    url(r'^registro/$', 'app.views.nuevo_usuario',name='registro'),
    url(r'^puntos/$', 'app.views.puntos',name='puntos'),
    url(r'^mispartidos/puntos/$', 'app.views.puntos',name='puntos'),
    url(r'^posiciones/puntos/$', 'app.views.puntos',name='puntos'),
    url(r'^pronosticos/$', 'app.views.pronosticos',name='pronosticos'),
    url(r'^pronosticos/puntos/$', 'app.views.puntos',name='puntos'),
    # Uncomment the next line to enable the admin:
    
)

