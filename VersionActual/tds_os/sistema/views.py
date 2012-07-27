from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import *
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db import IntegrityError
from django.db import DatabaseError
import json;

@transaction.commit_on_success
@login_required(login_url='/sistema/login')
def crearHistoria(request):
  
    if 'jornada_cod' not in request.session:
      return HttpResponseRedirect('/sistema/jornada')
      
    if 'mod_visualizar' in request.session and request.session["mod_visualizar"]=='html':
        codigo_jornada=request.session['jornada_cod']
        if request.POST:
	    
            try:
                fecha_n = request.POST["anyo"]+"-"+request.POST["mes"]+"-"+request.POST["dia"]
                p=Paciente.objects.create(
                          nombre_completo = request.POST["nombres"],
                    	fecha_nacimiento = fecha_n,
                    	edad             = request.POST["edad"],
                    	genero          = request.POST["sexo"],
                    	direccion       = request.POST["dir"],
                    	pais            = request.POST["pais"])
                p.save()
                j=Jornada.objects.get(codigo=codigo_jornada)
                asiste=Asiste.objects.create(
                          paciente = p,
                    	jornada  = j,
                    	r_nombre_completo = request.POST["acompanante"])
                asiste.save()
                h=Historia.objects.create(
                         paciente         =  p,
                         nro_historia     =  request.POST["exp"].strip())
                h.save()
                return render_to_response('sistema/historiaHTML.html',
                    {'mensaje': 'Historia Agregada con Exito','esCreacion' : True,},
                context_instance=RequestContext(request))
            except IntegrityError,e:
                transaction.rollback()
                return render_to_response('sistema/historiaHTML.html',
                    {'mensaje': 'Error al crear paciente :'+str(e),'esCreacion' : True,'codigo_j' : codigo_jornada,},
                    context_instance=RequestContext(request))
        else:
            return render_to_response('sistema/historiaHTML.html',
                    {'codigo_j' : codigo_jornada,'esCreacion' : True,},
                    context_instance=RequestContext(request))
    else:
        if request.POST and ('jornada_cod' in request.session):
            try:
                p=Paciente.objects.create(
                            nombre_completo = request.POST["nombre_paciente"])
                p.save()
                j=Jornada.objects.get(codigo=request.session['jornada_cod'])
                asiste=Asiste.objects.create(
                      paciente = p,
                      jornada  = j,)
                asiste.save()
                h=Historia.objects.create(
                         paciente         =  p,
                         nro_historia     =  request.POST["nroHistoria"].strip())

                h.save()
                if 'archivo'  in request.FILES:
                    nombre_archivo=request.FILES['archivo'].name.replace(' ', '')
                    contiene=Contiene.objects.create(
                        historia = h,
                        jornada  = j,
                        directorio='media/archivos/archivos_pdf/'+j.codigo+'/'+request.POST["nroHistoria"],
                        nombre=nombre_archivo,
                        tipo=request.POST["tipo"]
                        )
                    contiene.save()
                    contiene.file.save(nombre_archivo,request.FILES['archivo'])
                    contiene.save()
                    return render_to_response('sistema/crearH.html',
                    {'mensaje': 'Historia Creada','codigo_j':j.codigo,},context_instance=RequestContext(request))
                else:
                    return render_to_response('sistema/crearH.html',
                    {'mensaje': 'Historia Creada','codigo_j':j.codigo,},context_instance=RequestContext(request))
                return render_to_response('sistema/crearH.html',
                    {'mensaje': 'Historia Creada a','codigo_j':j.codigo,},
                    context_instance=RequestContext(request))
            except IntegrityError,e:
                transaction.rollback()
                return render_to_response('sistema/crearH.html',
                    {'mensaje': 'Error al agregar paciente'+str(e),'codigo_j':j.codigo,},
                    context_instance=RequestContext(request))
        else:
	    cod_j = request.session['jornada_cod']
	    j=Jornada.objects.get(codigo=cod_j)
            return render_to_response('sistema/crearH.html',{'jornada':j,},
            context_instance=RequestContext(request))


@login_required(login_url='/sistema/login')
def historiaB(request):
    if request.POST:
        if request.POST["centinela"] == 'historia':
            h_nro = request.POST["nro_historia"]
            n = request.POST["nombre_paciente"]
            pacientes = []
            historias = []
            if n != '':
                pacientes= Paciente.objects.filter(nombre_completo__icontains=n)
            historia_p = [(x.nombre_completo, x.historia_set.all()[0]) for x in pacientes]
            if h_nro != '':
	      historias = Historia.objects.filter(nro_historia=h_nro)
            return render_to_response('sistema/historiaB.html',
            {'lista_historia': historias, 'lista_paciente': historia_p,
                 'busquedaH': True},
            context_instance=RequestContext(request))
        else:
            return render_to_response('sistema/historiaB.html',
            context_instance=RequestContext(request))
            #return HttpResponseRedirect(reverse('sistema.views.historia',
            #args=(h_id,)))
    else:
        return render_to_response('sistema/historiaB.html',
        context_instance=RequestContext(request))
        

@login_required(login_url='/sistema/login')
def agregar_paciente(request):
    if 'jornada_cod' not in request.session:
      return HttpResponseRedirect('/sistema/jornada')
      
    cod_j = request.session['jornada_cod']
    j=Jornada.objects.get(codigo=cod_j)
    
    if 'error' in request.session:
        if request.session["error"][0]:
            mensaje=request.session["error"][1]
            request.session["error"]=(False,'')
            return render_to_response('sistema/agregarPaciente.html',
                {'mensaje':mensaje,'jornada':j,},
            context_instance=RequestContext(request))

    if 'correcto' in request.session:
        if request.session["correcto"][0]:
            mensaje=request.session["correcto"][1]
            request.session["correcto"]=(False,'')
            return render_to_response('sistema/agregarPaciente.html',
                {'mensaje':mensaje,'jornada':j,},
            context_instance=RequestContext(request))

    if request.POST:
        h_nro = request.POST["nro_historia"]
        n = request.POST["nombre_paciente"]
        pacientes = []
        historias = []
        if n != '':
            pacientes= Paciente.objects.filter(nombre_completo__icontains=n)
	historia_p = [(x.nombre_completo, x.historia_set.all()[0]) for x in pacientes]
        if h_nro != '':
	  historias = Historia.objects.filter(nro_historia=h_nro)
        return render_to_response('sistema/agregarPaciente.html',
            {'lista_historia': historias, 'lista_paciente': historia_p,
                 'busquedaH': True,'jornada':j},
        context_instance=RequestContext(request))
    else:
        return render_to_response('sistema/agregarPaciente.html',{'jornada':j},
        context_instance=RequestContext(request))


def agregar_paciente_id(request, h_id):
    if 'jornada_cod' in request.session:
        try:
            cod_j = request.session['jornada_cod']
            j=Jornada.objects.get(codigo=cod_j)
            h=Historia.objects.get(nro_historia=h_id)
            nuevo_p=h.paciente
            pacientes=j.pacientes.all()
            for p in pacientes:
                if p.id_paciente==nuevo_p.id_paciente:
                    request.session['error']=(True,'Paciente '+nuevo_p.nombre_completo+' ya pertenece a la jornada')
                    return HttpResponseRedirect('/sistema/agregarPaciente')
            asiste=Asiste.objects.create(
                          paciente = nuevo_p,
                          jornada  = j)
            asiste.save()
            request.session['correcto']=(True,'Paciente agregado a la jornada')
            return HttpResponseRedirect('/sistema/agregarPaciente')
        except DatabaseError:
            request.session['error']=(True,'Hubo un error al tratar de agregar al paciente')
            return HttpResponseRedirect('/sistema/agregarPaciente')
    else:
        return HttpResponseRedirect('/sistema/agregarPaciente')


def autocomplete_historia(request):
    if request.is_ajax():
        historias_obj = Historia.objects.all()
        cod_historias = []
        for h in historias_obj:
            cod_historias.append(h.nro_historia)
        data = json.dumps(cod_historias)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    else:
        data ='fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)



def autocomplete_paciente(request):
    if request.is_ajax():
        pacientes_obj = Paciente.objects.all()
        name_pacientes=[]
        for p in pacientes_obj:
            name_pacientes.append(p.nombre_completo)
        data = json.dumps(name_pacientes)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    else:
        data='fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


def autocomplete_jornada(request):
    if request.is_ajax():
        jornada_obj = Jornada.objects.all()
        codigos_jornada=[]
        for j in jornada_obj:
            codigos_jornada.append(j.codigo)
        data = json.dumps(codigos_jornada)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    else:
        data='fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)



def busqueda(request):
    if request.POST:
        if request.POST["centinela"] == 'historia':
            h_nro = request.POST["nro_historia"]
            n = request.POST["nombre_paciente"]
            pacientes = []
            if n != '':
                pacientes= Paciente.objects.filter(nombre_completo__icontains=n)
            historia_p = [(x.nombre_completo, x.historia_set.all()[0])
            for x in pacientes]
            historias = Historia.objects.filter(nro_historia=h_nro)
            return render_to_response('sistema/busqueda.html',
            {'lista_historia': historias, 'lista_paciente': historia_p,
                 'busquedaH': True},
            context_instance=RequestContext(request))
            #return HttpResponseRedirect(reverse('sistema.views.historia',
            #args=(h_id,)))
        else:
            jornada_cod = request.POST["jornada_codigo"]
            jornadas = Jornada.objects.filter(codigo=jornada_cod)
            return render_to_response('sistema/busqueda.html',
            {'lista_jornada': jornadas, 'busquedaJ': True},
            context_instance=RequestContext(request))
            #return HttpResponseRedirect(reverse('sistema.views.historia',
            #args=(h_id,)))
    else:
        return render_to_response('sistema/busqueda.html',
        context_instance=RequestContext(request))


@login_required(login_url='/sistema/login')
def paciente_jornadas(request,h_id):
    h = get_object_or_404(Historia, nro_historia=h_id)
    try:
        p = h.paciente
        jornadas = p.jornada_set.all()
        return render_to_response('sistema/paciente_jornadas.html',
               {'historia_id': h.nro_historia, 'paciente': p, 'lista_jornada': jornadas,},
               context_instance=RequestContext(request))
    except (KeyError, Historia.DoesNotExist):
        return render_to_response('sistema/historiaB.html', {
            'error_message': "La historia solicitada no existe",
            'restart': True,
        }, context_instance=RequestContext(request, {'restart': True, }))


@login_required(login_url='/sistema/login')
def paciente_documentos(request, j_codigo, h_id):
    try:
        h = get_object_or_404(Historia, nro_historia=h_id)
        p = h.paciente
        j = p.jornada_set.all().get(codigo=j_codigo)
        c = h.contiene_set.all()
        if 'mod_visualizar' in request.session and request.session["mod_visualizar"]=='html':
            a = p.asiste_set.all()
            mensaje=""
            asiste=a.filter(jornada=j_codigo)
            fecha=["" for x in range(0,3)]
            if p.fecha_nacimiento:
	      fecha=p.fecha_nacimiento.strftime("%Y-%m-%d")
	      fecha=fecha.split('-')
	    if request.POST:
	      p.edad=request.POST["edad"]
	      p.direccion=request.POST["dir"]
	      p.save()
	      mensaje="Datos Actualizados"
            return render_to_response('sistema/historiaHTML.html',
                       {'historia': h, 'paciente': p, 'jornada': j,'asiste_info':asiste,
                        'ano':fecha[0],'mes':fecha[1],'dia':fecha[2],'mensaje':mensaje,},
                       context_instance=RequestContext(request))
        if request.POST:
            try:
                if 'archivo'  in request.FILES:
                    nombre_archivo=request.FILES['archivo'].name.replace(' ', '')
                    contiene=Contiene.objects.create(
                        historia = h,
                        jornada  = j,
                        directorio='archivos/archivos_pdf/'+j_codigo+'/'+h_id,
                        nombre=nombre_archivo,
                        tipo=request.POST["tipo"]
                        )
                    contiene.save()
                    contiene.file.save(nombre_archivo,request.FILES['archivo'])
                    contiene.save()
                    return render_to_response('sistema/paciente_documentos.html',
                    {'mensaje': 'Archivo Agregado','historia': h.nro_historia,
                     'paciente': p, 'jornada': j,},
                    context_instance=RequestContext(request))
                else:
                    return render_to_response('sistema/paciente_documentos.html',
                    {'mensaje': 'Error al agregar archivo','historia': h.nro_historia,
                     'paciente': p, 'jornada': j,},
                    context_instance=RequestContext(request))
            except IntegrityError, e:
                transaction.rollback()
                return render_to_response('sistema/paciente_documentos.html',
                    {'mensaje': 'Error al agregar archivo'+str(e),},
                    context_instance=RequestContext(request))
        else:
            documentos_j= c.filter(jornada=j_codigo)
            return render_to_response('sistema/paciente_documentos.html',
                       {'historia': h.nro_historia, 'paciente': p, 'jornada': j, 'documentos_jornada': documentos_j, },
                       context_instance=RequestContext(request))
    except (KeyError, Historia.DoesNotExist):
            return HttpResponseRedirect('/sistema/historia')



@login_required(login_url='/sistema/login')
def historia(request, j_codigo, h_id):
    h = get_object_or_404(Historia, nro_historia=h_id)
    try:
        p = h.paciente
        j = p.jornada_set.all()[0]
        a = p.asiste_set.all()[0]
        return render_to_response('sistema/historia.html',
               {'historia': h, 'paciente': p, 'jornada': j, 'asiste': a, },
               context_instance=RequestContext(request))
    except (KeyError, Historia.DoesNotExist):
        return render_to_response('sistema/historiaB.html', {
            'error_message': "La historia solicitada no existe",
            'restart': True,
        }, context_instance=RequestContext(request, {'restart': True, }))


def paciente(request, p_id):
    p = Paciente.objects.get(id_paciente=p_id)
    return render_to_response('sistema/historia.html',
    {'historia': p}, context_instance=RequestContext(request))


@login_required(login_url='/sistema/login')
def jornadaB(request):
    if request.POST:
        jornada_cod = request.POST["jornada_codigo"]
        jornadas = Jornada.objects.filter(codigo=jornada_cod)
        return render_to_response('sistema/jornadaB.html',
        {'lista_jornada': jornadas, 'busquedaJ': True},
        context_instance=RequestContext(request))
        #historias = Jornada.objects.get(codigo=jornada_cod)
        #return render_to_response('sistema/historiaB.html',
        #{'lista_historia': historias, 'busqueda': True},
        #context_instance=RequestContext(request))
    else:
        return render_to_response('sistema/jornadaB.html',
        context_instance=RequestContext(request))


@login_required(login_url='/sistema/login')
def jornada(request, j_id):
    #j = get_object_or_404(Jornada, codigo=j_id)
    try:

        j = Jornada.objects.get(codigo=j_id)
        request.session['jornada_cod'] = j.codigo
        lista_p = j.pacientes.all()
        lista_p = [(x, x.historia_set.all()[0]) for x in lista_p]
        return render_to_response('sistema/jornada.html',
               {'lista_pacientes': lista_p, 'jornada': j},
               context_instance=RequestContext(request))
    except (KeyError, Jornada.DoesNotExist):
        return render_to_response('sistema/jornadaB.html', {
            'error_message': 'La jornada ' + j_id + " no existe",
             }, context_instance=RequestContext(request))

@transaction.commit_on_success
@login_required(login_url='/sistema/login')
def crear_jornada(request):
    if request.POST:
        try:
            jornada=Jornada.objects.create(
                    codigo = request.POST["codigo_jornada"].strip(),
                    name   = request.POST["nombre_jornada"],
                    fecha  = request.POST["fecha_jornada"],
                    ciudad = request.POST["ciudad_jornada"]
                )
            return render_to_response('sistema/crear_jornada.html',
                   {'mensaje': 'Jornada creada', 'jornada': jornada},
                   context_instance=RequestContext(request))
        except IntegrityError:
            return render_to_response('sistema/crear_jornada.html',
                   {'mensaje': 'La jornada ya existe',},
                   context_instance=RequestContext(request))
        except DatabaseError,e:
            return render_to_response('sistema/crear_jornada.html',
                   {'mensaje': 'Ha ocurrido un error'+str(e),},
                   context_instance=RequestContext(request))
    else:
        return render_to_response('sistema/crear_jornada.html',
                   context_instance=RequestContext(request))

@login_required(login_url='/sistema/login')
def opciones(request):
    mensaje=""
    if request.GET:
        request.session["mod_visualizar"]=request.GET["opcion"]
        mensaje=request.session["mod_visualizar"]
    return render_to_response('sistema/opciones.html',{'mensaje': mensaje},
           context_instance=RequestContext(request))

@login_required(login_url='/sistema/login')          
def planillasModelos(request):
  return render_to_response('sistema/planillasModelo.html',
           context_instance=RequestContext(request))
    
