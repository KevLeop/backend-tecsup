create database bdprueba;

use bdprueba;

# create schema bdprueba; #solo en mysql


create table t_categoria(
	# Solo puede haber una columna con auto_increment,
	categoria_id int primary key not null auto_increment,
    categoria_nombre varchar(25) unique
);

create table t_producto(
	producto_id int primary key not null auto_increment,
    producto_nombre varchar(25) unique not null,
    producto_precio float(5,2) not null,
    producto_cantidad int not null,
    categoria_id int not null,
    foreign key (categoria_id) references t_categoria(categoria_id)
);

insert into t_categoria (categoria_nombre) values ('Abarrotes');
insert into t_categoria (categoria_nombre) values ('Pastas'),('Limpieza'),('Mascotas'),('Higiene');

insert into t_producto values (1,'Lejia',3.40,50,1);
insert into t_producto values (50,'Canelon',1.80,25,2);
insert into t_producto (producto_nombre, producto_precio, producto_cantidad, categoria_id) values
						('RicoDog 1KG',5.40,15,4),
                        ('Pasta Dental',3.80,20,5);
insert into t_producto (producto_nombre, producto_precio, producto_cantidad, categoria_id) values
						('Ricocan',6.40,20,4),
                        ('Pasta Dental Colgate',3.50,120,5);

select * from t_categoria;
select * from t_producto;
