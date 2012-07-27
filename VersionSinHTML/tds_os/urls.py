from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sistema/login$', 'django.contrib.auth.views.login',
       {'template_name': 'sistema/login.html'}),
   # url(r'^sistema/login$', 'sistema.views.index'),
    url(r'^sistema/crearHistoria$', 'sistema.views.crearHistoria'),
    url(r'^sistema/busqueda$', 'sistema.views.busqueda'),
    url(r'^sistema/historia$', 'sistema.views.historiaB'),
    url(r'^sistema/agregarPaciente$', 'sistema.views.agregar_paciente'),
    url(r'^sistema/agregarPaciente/(?P<h_id>\w+)/$', 'sistema.views.agregar_paciente_id'),
    url(r'^sistema/autocomplete_p$', 'sistema.views.autocomplete_paciente'),
    url(r'^sistema/autocomplete_j$', 'sistema.views.autocomplete_jornada'),
    url(r'^sistema/autocomplete_h$', 'sistema.views.autocomplete_historia'),
    url(r'^sistema/historia/(?P<j_codigo>\w+)/(?P<h_id>\w+)/$', 'sistema.views.historia'),
    url(r'^sistema/paciente_documentos/(?P<j_codigo>\w+)/(?P<h_id>\w+)/$', 'sistema.views.paciente_documentos'),
    url(r'^sistema/paciente_jornadas/(?P<h_id>\w+)/$', 'sistema.views.paciente_jornadas'),
    url(r'^sistema/paciente/(?P<p_id>\w+)/$', 'sistema.views.paciente'),
    url(r'^sistema/jornada$', 'sistema.views.jornadaB'),
    url(r'^sistema/jornada/(?P<j_id>\w+)/$', 'sistema.views.jornada'),
    url(r'^sistema/crearJornada$', 'sistema.views.crear_jornada'),
    url(r'^sistema/opciones$', 'sistema.views.opciones'),
    url(r'^sistema/planillasModelos$', 'sistema.views.planillasModelos'),    
    # Examples:
    # url(r'^$', 'tds_os.views.home', name='home'),
    # url(r'^tds_os/', include('tds_os.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
