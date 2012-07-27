BEGIN;
CREATE TABLE "sistema_paciente" (
    "id_paciente" serial NOT NULL PRIMARY KEY,
    "nombre_completo" varchar(100) NOT NULL,
    "fecha_nacimiento" date NOT NULL,
    "lugar_nacimiento" varchar(50) NOT NULL,
    "edad" integer NOT NULL,
    "genero" varchar(2) NOT NULL,
    "escolaridad" varchar(50),
    "direccion" varchar(150) NOT NULL,
    "ciudad" varchar(50) NOT NULL,
    "estado" varchar(50) NOT NULL,
    "pais" varchar(30) NOT NULL,
    "num_hermanos" integer,
    "vive_con" varchar(30),
    "familia_con_LoPH" boolean NOT NULL
)
;
CREATE TABLE "sistema_jornada" (
    "codigo" varchar(100) NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "fecha" date NOT NULL,
    "ciudad" varchar(50) NOT NULL
)
;
CREATE TABLE "sistema_asiste" (
    "id" serial NOT NULL PRIMARY KEY,
    "paciente_id" integer NOT NULL REFERENCES "sistema_paciente" ("id_paciente") DEFERRABLE INITIALLY DEFERRED,
    "jornada_id" varchar(100) NOT NULL REFERENCES "sistema_jornada" ("codigo") DEFERRABLE INITIALLY DEFERRED,
    "r_ci" integer NOT NULL,
    "r_nombre_completo" varchar(100) NOT NULL,
    "r_grado_instruccion" varchar(20) NOT NULL,
    "r_profesion" varchar(50) NOT NULL,
    "r_direccion" varchar(150) NOT NULL,
    "r_telefono" integer NOT NULL,
    "r_email" varchar(100) NOT NULL
)
;
CREATE TABLE "sistema_historia" (
    "nro_historia" integer NOT NULL PRIMARY KEY,
    "medic_actual" varchar(50) NOT NULL,
    "alergias" varchar(50) NOT NULL,
    "embarazada" varchar(30) NOT NULL,
    "infecciones" varchar(50) NOT NULL,
    "cns" varchar(50) NOT NULL,
    "pulmones" varchar(30) NOT NULL,
    "corazon" varchar(30) NOT NULL,
    "lab_hematocritos" varchar(50) NOT NULL,
    "lab_hemoglobina" varchar(50) NOT NULL,
    "lab_otros" varchar(100) NOT NULL,
    "tipo_prestamo" varchar(50) NOT NULL,
    "estado" varchar(30) NOT NULL
)
;
CREATE TABLE "sistema_operacion" (
    "id" serial NOT NULL PRIMARY KEY,
    "resultado" varchar(500) NOT NULL,
    "tipo_id" integer NOT NULL REFERENCES "sistema_historia" ("nro_historia") DEFERRABLE INITIALLY DEFERRED,
    "fecha" date NOT NULL,
    "lugar" varchar(100) NOT NULL,
    "hora" timestamp with time zone NOT NULL
)
;
CREATE TABLE "sistema_posee" (
    "id" serial NOT NULL PRIMARY KEY,
    "historia_id" integer NOT NULL REFERENCES "sistema_historia" ("nro_historia") DEFERRABLE INITIALLY DEFERRED,
    "jornada_id" varchar(100) NOT NULL REFERENCES "sistema_jornada" ("codigo") DEFERRABLE INITIALLY DEFERRED,
    "codigo" varchar(50) NOT NULL UNIQUE,
    "diag_labio" varchar(50) NOT NULL,
    "diag_paladar" varchar(50) NOT NULL,
    "diag_fistulas" varchar(50) NOT NULL,
    "diag_nariz" varchar(50) NOT NULL,
    "diag_dientes" varchar(50) NOT NULL,
    "diag_otros" varchar(50) NOT NULL,
    "requiere_oper" boolean NOT NULL
)
;
CREATE TABLE "sistema_contiene" (
    "historia_id" integer NOT NULL REFERENCES "sistema_historia" ("nro_historia") DEFERRABLE INITIALLY DEFERRED,
    "jornada_id" varchar(100) NOT NULL REFERENCES "sistema_jornada" ("codigo") DEFERRABLE INITIALLY DEFERRED,
    "codigo" varchar(50) NOT NULL PRIMARY KEY,
    "nombre" varchar(50) NOT NULL,
    "tipo" varchar(50) NOT NULL
)
;
COMMIT;
