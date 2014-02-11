from django.shortcuts import render_to_response,get_object_or_404, render
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from .models import Fecha, Resultado, Partido, PartidoFinal, Usuario, FechaAJugar, TablaFecha
from django.contrib.auth.models import User
from datetime import date
from django.views.generic import TemplateView, FormView
from .forms import UserForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout





def nuevo_usuario(request):
	registrado=False
	if request.method =='POST':
		template="inicio.html"
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid:
			registrado=True
			formulario.save()
			print registrado
			return HttpResponseRedirect("/")
	else:
		formulario = UserCreationForm()
	return render_to_response('registrarse.html',{'formulario':formulario}, context_instance=RequestContext(request))







def mispartidos(request):
	fechaO = FechaAJugar.objects.all()
	for f in fechaO:
		fechaJugada= f.fechaEnJuego
	
	
	template = "dashboard.html"
	resultados = Resultado.objects.filter( usuario = request.user ).filter(fecha=fechaJugada)
	usuarioMoroso = get_object_or_404(Usuario, usuario = request.user)
	partidos = Partido.objects.order_by('fechaPartido').filter(fecha=fechaJugada)
	tablafecha = TablaFecha.objects.order_by('-puntos').filter(fecha=fechaJugada)
	fechaObject = get_object_or_404(Fecha, fecha=fechaJugada)
	usuarioTabla = get_object_or_404(User, username= request.user)
	desactivar = False
	if date.today() >= fechaObject.fechaInicio:
		desactivar =True

	print usuarioMoroso.moroso
	for r in resultados:
		if r.fechaGuardada:
			fg = True
		else:
			fg = False

	if request.POST:
		for p in partidos:
			usuario = get_object_or_404(User, username= request.user)
			fecha = get_object_or_404(Fecha, fecha=p.fecha)
			equipoLocal = p.local
			resultadoLocal = request.POST[p.sluglocal]
			equipoVisit = p.visitante
			resultadoVisit = request.POST[p.slugvisitante]
			puntos = 0
			Guardada =True
			resultado = Resultado (usuario = usuario, fecha =fecha, local=equipoLocal, marcadorLocal=resultadoLocal, visitante = equipoVisit, marcadorVisitante = resultadoVisit, puntos = puntos, fechaGuardada = Guardada )
			resultado.save()
			fg = True
		return HttpResponseRedirect("/")


			
	else:
		print "No Hizo request POST"

	
	dicUsuario = {}
	usuariosJ = Usuario.objects.all()
	resultadosJ = Resultado.objects.filter(fecha=fechaJugada)
	varu=False
	for u in usuariosJ:

		i=0
		for r in resultadosJ:
			if u.usuario==r.usuario:
				i=i+1
			if i==9:
				dicUsuario[r.usuario] = r.usuario

	print dicUsuario
	return render_to_response(template,context_instance=RequestContext(request,locals()))


def administracion(request):
	fechaO = FechaAJugar.objects.all()
	for f in fechaO:
		fechaJugada= f.fechaEnJuego
	partidos = Partido.objects.order_by('fechaPartido').filter(fecha=fechaJugada)
	print partidos
	template = "administracion.html"
	if request.POST:
		for p in partidos:
			usuario = get_object_or_404(User, username= request.user)
			fecha = get_object_or_404(Fecha, fecha=p.fecha)
			equipoLocal = p.local
			resultadoLocal = request.POST[p.sluglocal]
			equipoVisit = p.visitante
			resultadoVisit = request.POST[p.slugvisitante]
			resultadoFinal = PartidoFinal (fecha = fecha, local= equipoLocal, marcadorLocal=resultadoLocal, visitante = equipoVisit, marcadorVisitante=resultadoVisit, fechaPartido= date.today())
			resultadoFinal.save()

		return HttpResponseRedirect("/")
			
	else:
		print "No Hizo request POST"



	return render_to_response(template,context_instance=RequestContext(request,locals()))







def vertabla(request):
	pcal =False
	fechaO = FechaAJugar.objects.all()

	for f in fechaO:
		fechaJugada= f.fechaEnJuego

	partidosFinales = PartidoFinal.objects.order_by('fechaPartido').filter(fecha=fechaJugada)
	usuarios = Usuario.objects.all()
	for u in usuarios:
		print u.usuario
		resultados = Resultado.objects.filter( usuario = u.usuario ).filter(fecha=fechaJugada)
		puntaje = 0
		for pf in partidosFinales:

			for res in resultados:
				print pf.local
				print res.local 
				print pf.visitante
				print res.visitante
				print res.puntajeCalculado
				if pf.local == res.local and pf.visitante == res.visitante and res.puntajeCalculado==False:
					res.puntajeCalculado =True
					print "Sii entro"
					pcal = True
					if pf.marcadorLocal == res.marcadorLocal and pf.marcadorVisitante == res.marcadorVisitante:
						puntaje = puntaje + 4
						res.puntos = 4
					elif pf.marcadorLocal> pf.marcadorVisitante and res.marcadorLocal> res.marcadorVisitante:
						puntaje = puntaje + 2
						res.puntos = 2
					elif pf.marcadorLocal< pf.marcadorVisitante and res.marcadorLocal< res.marcadorVisitante:
						puntaje = puntaje + 2
						res.puntos = 2
					else:
						resultado1 = pf.marcadorLocal - pf.marcadorVisitante
						resultado2 = res.marcadorLocal - res.marcadorVisitante
						if resultado1 == 0 and resultado2 == 0:
							puntaje = puntaje + 2
							res.puntos = 2
							
					res.save()
	


		usuarioPuntaje = get_object_or_404(Usuario, usuario = u.usuario)
		usuarioPuntaje.puntos = usuarioPuntaje.puntos + puntaje
		usuarioPuntaje.save()


	for u in usuarios:
		resultados = Resultado.objects.filter( usuario = u.usuario ).filter(fecha=fechaJugada)
		tablafecha = TablaFecha.objects.filter(usuario=u.usuario).filter(fecha=fechaJugada)
		puntajeFecha = 0
		
		for res in resultados:
			if res.fechaGuardada:
				puntajeFecha = puntajeFecha + res.puntos
				

		if tablafecha:
			tablafU= get_object_or_404(TablaFecha, usuario=u.usuario)
			
			tablafU.puntos = puntajeFecha
			tablafU.save()
		else:
			fecha = get_object_or_404(Fecha, fecha=fechaJugada)
			tablaf = TablaFecha (fecha=fecha, usuario=u.usuario, puntos=puntajeFecha )
			tablaf.save()
	

	return HttpResponseRedirect("/")


def posiciones(request):
	fechaO = FechaAJugar.objects.all()
	for f in fechaO:
		fechaJugada= f.fechaEnJuego
		
	tabla = Usuario.objects.order_by('-puntos')
	mayor = 0
	puntajeFecha = 0
	usuarios = Usuario.objects.all()
	ganador = False
	usuarioTabla = get_object_or_404(User, username= request.user)



	template = "tabla.html"
	return render_to_response(template,context_instance=RequestContext(request,locals()))

from django.core import serializers
def puntos(request):
	usuarioP= get_object_or_404(User, username= request.user)
	puntosO = Usuario.objects.filter(usuario=usuarioP)
	data = serializers.serialize('json',puntosO, fields=('puntos'))
	return HttpResponse(data, mimetype='application/json')



def pronosticos(request):
	fechaO = FechaAJugar.objects.all()
	for f in fechaO:
		fechaJugada= f.fechaEnJuego
	fechaObject = get_object_or_404(Fecha, fecha=fechaJugada)
	if date.today() >= fechaObject.fechaInicio:
		activarPronostico=True

	dicUsuario = {}
	usuarios = Usuario.objects.all()
	resultados = Resultado.objects.filter(fecha=fechaJugada)
	varu=False
	for u in usuarios:

		i=0
		for r in resultados:
			if u.usuario==r.usuario:
				i=i+1
			if i==9:
				dicUsuario[r.usuario] = r.usuario
			



	template = "pronosticos.html"
	return render_to_response(template,context_instance=RequestContext(request,locals()))