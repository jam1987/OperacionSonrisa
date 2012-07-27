from sistema.models import *

Carbu = Paciente.objects.create(
            nombre_completo  = "Pedro",
            fecha_nacimiento = "2001-10-05",
            lugar_nacimiento = "Caracas",
            edad             = 11,
            genero           = "M",
            escolaridad      = "Primaria",
            direccion        = "En la esquina",
            ciudad           = "Caracas",
            estado           = "Distrito Capital",
            pais             = "Venezuela",
            num_hermanos     =  2,
            vive_con         = "padres",
            familia_con_LoPH = True)

historia_carbu = Historia.objects.create(
                 paciente         =  Carbu,
                 nro_historia     =  '9999',
                 medic_actual     =  "1",
                 alergias         =  "1",
                 embarazada       =  "Si",
                 infecciones      =  "2",
                 cns              =  "2,3",
                 pulmones         =  "Si",
                 corazon          =  "Si",
                 lab_hematocritos =  "hematocritos",
                 lab_hemoglobina  =  "hemoglobina",
                 lab_otros        =  "otros",
                 tipo_prestamo    =  "prestamo 1")

jornada_USB     = Jornada.objects.create(
                       codigo     =  66651474,
                       name       =  "Jornada USB",
                       fecha      =  "2012-08-01",
                       ciudad     =   "Caracas")


asiste1         = Asiste.objects.create(
                        paciente            =  Carbu,
                        jornada             =  jornada_USB,
                        r_ci                =  1875588,
                        r_nombre_completo   =  "Cantando Perez",
                        r_grado_instruccion =  "Universitario",
                        r_profesion         =  "Computista",
                        r_direccion         =  "En la esquina dos",
                        r_telefono          =  4828844,
                        r_email             =  "perez@hotmail.com")

posee1         = Posee.objects.create(
                        historia               =  historia_carbu,
                        jornada                =  jornada_USB,
                        diag_labio             =  "diag_labio",
                        diag_paladar           =  "diag_paladar",
                        diag_fistulas          =  "diag_fistulas",
                        diag_nariz             =  "diag_nariz",
                        diag_dientes           =  "diag_dientes",
                        diag_otros             =  "diag_otros",
                        requiere_oper          =  True)
posee1.save()
asiste1.save()
