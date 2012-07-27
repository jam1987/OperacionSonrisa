from django.db import models
from newFileField import ContentTypeRestrictedFileField
# Create your models here.




class Paciente(models.Model):
	GENERO_SELECT=(
	(u'M',u'Masculino'),(u'F',u'Femenino'),)
	id_paciente = models.AutoField(primary_key=True)
	nombre_completo = models.CharField(max_length=100)
	fecha_nacimiento= models.DateField(null=True)
	lugar_nacimiento= models.CharField(max_length=50)
	edad            = models.IntegerField(null=True)
	genero          = models.CharField(max_length=2,choices=GENERO_SELECT)
	escolaridad     = models.CharField(max_length=50, null=True)
	direccion       = models.CharField(max_length=150)
	ciudad          = models.CharField(max_length=50)
	estado          = models.CharField(max_length=50)
	pais            = models.CharField(max_length=30)
	num_hermanos    = models.IntegerField(null=True)
	vive_con        = models.CharField(max_length=30, null=True)
	familia_con_LoPH= models.BooleanField(default=0)
	def __unicode__(self):
		return self.nombre_completo


class Jornada(models.Model):
	codigo = models.CharField(max_length=100, primary_key=True)
	name   = models.CharField(max_length=50)
	fecha  = models.DateField()
	ciudad = models.CharField(max_length=50)
	pacientes = models.ManyToManyField(Paciente, through='Asiste')

	def __unicode__(self):
		return self.name

class Asiste(models.Model):
	paciente = models.ForeignKey(Paciente)
	jornada  = models.ForeignKey(Jornada)
	r_ci     = models.IntegerField(max_length=30,null=True)
	r_nombre_completo = models.CharField(max_length=100,null=True)
	r_grado_instruccion = models.CharField(max_length=20,null=True)
	r_profesion = models.CharField(max_length=50,null=True)
	r_direccion = models.CharField(max_length=150,null=True)
	r_telefono  = models.IntegerField(null=True)
	r_email     = models.CharField(max_length=100,null=True)




class Historia(models.Model):
	paciente                  = models.ForeignKey(Paciente)
	jornadas                  = models.ManyToManyField(Jornada, through='Posee')
	jornadas                  = models.ManyToManyField(Jornada, through='Contiene')
	nro_historia = models.CharField(max_length=30,primary_key=True)
	medic_actual = models.CommaSeparatedIntegerField(max_length=50)
	alergias     = models.CommaSeparatedIntegerField(max_length=50)
	embarazada   = models.CharField(max_length=30)
	infecciones  = models.CommaSeparatedIntegerField(max_length=50)
	cns          = models.CommaSeparatedIntegerField(max_length=50)
	pulmones     = models.CharField(max_length=30)
	corazon      = models.CharField(max_length=30)
	lab_hematocritos = models.CharField(max_length=50)
	lab_hemoglobina  = models.CharField(max_length=50)
	lab_otros        = models.CharField(max_length=100)
	tipo_prestamo    = models.CharField(max_length=50)
	estado           = models.CharField(max_length=30)
	def __unicode__(self):
		return nro_historia


class Operacion(models.Model):
	resultado = models.CharField(max_length=500)
	tipo      = models.ForeignKey(Historia)
	fecha     = models.DateField()
	lugar     = models.CharField(max_length=100)
	hora      = models.DateTimeField()


class Posee(models.Model):
	historia = models.ForeignKey(Historia)
	jornada  = models.ForeignKey(Jornada)
	codigo   = models.CharField(max_length=50, unique=True)
	diag_labio    = models.CharField(max_length=50)
	diag_paladar  = models.CharField(max_length=50)
	diag_fistulas = models.CharField(max_length=50)
	diag_nariz    = models.CharField(max_length=50)
	diag_dientes  = models.CharField(max_length=50)
	diag_otros    = models.CharField(max_length=50)
	requiere_oper = models.BooleanField(default=0)

class Contiene (models.Model):
	historia = models.ForeignKey(Historia)
	jornada  = models.ForeignKey(Jornada)
	nombre = models.CharField(max_length=300)
	directorio = models.CharField(max_length=300,default="")
	tipo   = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=250)
	file = ContentTypeRestrictedFileField(
	upload_to=' ',
	content_types=['application/pdf', 'application/zip'],
	max_upload_size=9000000
	)
	creacion_fecha = models.DateTimeField('created', auto_now_add=True)

        def save(self, *args, **kwargs):
            for field in self._meta.fields:
                        if field.name == 'file':
                            field.upload_to = self.directorio
            super(Contiene, self).save()
