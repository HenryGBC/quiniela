from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class Fecha(models.Model):
	fecha = models.CharField(max_length = 2)
	fechaInicio = models.DateField()
	fechaFin = models.DateField()

	def __unicode__(self):
		return self.fecha



class Resultado(models.Model):
	usuario = models.ForeignKey(User)
	fecha = models.ForeignKey(Fecha)
	local = models.CharField(max_length = 100)
	marcadorLocal = models.IntegerField(default = 0)
	visitante = models.CharField(max_length = 100)
	marcadorVisitante = models.IntegerField(default = 0)
	puntos = models.IntegerField()
	fechaGuardada = models.BooleanField(default = False)
	puntajeCalculado = models.BooleanField(default = False)
	def __unicode__(self):
		return "%s -  %s" % (self.usuario, self.fecha)


class Partido(models.Model):
	fecha = models.ForeignKey(Fecha)
	local = models.CharField(max_length=100)
	visitante = models.CharField(max_length=100)
	fechaPartido= models.DateField()
	sluglocal = models.SlugField(max_length=100, blank=True)
	slugvisitante = models.SlugField(max_length=100, blank=True)

	def save(self, *args, **kwargs):
		self.sluglocal = self.local.lower().replace(' ','-')
		self.slugvisitante = self.visitante.lower().replace(' ','-')
		super(Partido, self).save(*args, **kwargs)

	def __unicode__(self):
		return"%s - %s - %s " % (self.fecha, self.local, self.visitante)


class PartidoFinal(models.Model):
	fecha = models.ForeignKey(Fecha)
	local = models.CharField(max_length=100)
	marcadorLocal = models.IntegerField(default = 0)
	visitante = models.CharField(max_length=100)
	marcadorVisitante = models.IntegerField(default = 0)
	fechaPartido= models.DateField()

	def __unicode__(self):
		return"%s - %s - %s " % (self.fecha, self.local, self.visitante)



class Usuario(models.Model):
	usuario = models.ForeignKey(User)
	nombre = models.CharField(max_length= 100)
	moroso = models.BooleanField(default=False)
	puntos = models.IntegerField()

	def __unicode__(self):
		return self.nombre

class FechaAJugar(models.Model):
	fechaEnJuego = models.CharField(max_length= 2)

	def __unicode__(self):
		return "Fecha %s en juego" % (self.fechaEnJuego)

class TablaFecha(models.Model):
	fecha = models.ForeignKey(Fecha)
	usuario = models.ForeignKey(User)
	puntos = models.IntegerField(default=0)

	def __unicode__(self):
		return "%s - %s - %s" %(self.fecha, self.usuario, self.puntos)