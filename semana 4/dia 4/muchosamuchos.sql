create database if not exists muchosamuchos;
# drop database muchosamuchos; 
use muchosamuchos;

create table if not exists t_alumno(
	alum_id int primary key not null auto_increment,
    alum_nombre varchar(50) not null,
    alum_apellido varchar(50) not null,
    alum_grado varchar(10),
    alum_fec_nacimiento date);
    
create table if not exists t_curso(
	cur_id int primary key not null auto_increment,
    cur_nom varchar(30) not null,
    cur_dificultad varchar(25) not null);
    
    
create table if not exists t_alumno_curso(
	alum_id int not null,
    cur_id int not null,
    foreign key (alum_id) references t_alumno(alum_id),
    foreign key (cur_id) references t_curso(cur_id)
);

insert into t_alumno (alum_nombre, alum_apellido, alum_grado, alum_fec_nacimiento) values 
                    ('Eduardo','Juarez','Quinto','1992-08-01'),
                    ('Christopher','Rodriguez','Cuarto','1993-07-10'),
                    ('Raul','Pinto','Primero','1996-02-05'),
                    ('Cristina','Espinoza','Quinto','1992-10-21'),
                    ('Valeria','Acevedo','Cuarto','1993-05-18');

insert into t_curso (cur_nom, cur_dificultad) values
                    ('Matematica I','Facil'),
                    ('Fisica I','Facil'),
                    ('Matematica II','Intermedio'),
                    ('CTA','Dificil'),
                    ('Biologia','Dificil');
                    
insert into t_alumno_curso (alum_id, cur_id) values
							(1,2),(4,2), # todos los de quinto llevan Fisica I
							(1,4),(4,4), # todos los de quinto llevan CTA
							(2,3),(5,3), # todos los de cuarto llevan Matematica II
							(2,5),(5,5), # todos los de cuarto llevan Biologia
							(3,1),(3,3); # todos los de primero llevan Matematica I y Matematica II 

select alum_nombre Nombre, alum_apellido Apellido from t_alumno where alum_nombre="Eduardo";

select alum_nombre,alum_apellido,alum_grado,cur_nom 
from t_alumno as A inner join t_alumno_curso as C on C.alum_id = A.alum_id
inner join t_curso on t_curso.cur_id = C.cur_id
where C.cur_id = 2;







