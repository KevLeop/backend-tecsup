# Generated by Django 3.1.7 on 2021-03-18 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteModel',
            fields=[
                ('clienteDni', models.CharField(db_column='cli_dni', max_length=9, primary_key=True, serialize=False, unique=True)),
                ('clienteNombre', models.CharField(db_column='cli_nombre', max_length=45)),
                ('clienteApellido', models.CharField(db_column='cli_apellido', max_length=45)),
                ('clienteEmail', models.EmailField(db_column='cli_email', max_length=45)),
                ('clienteFono', models.CharField(db_column='cli_fono', max_length=15)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 't_cliente',
            },
        ),
        migrations.CreateModel(
            name='PromocionModel',
            fields=[
                ('promociionId', models.AutoField(db_column='promo_id', primary_key=True, serialize=False, unique=True)),
                ('promocionDescripcion', models.CharField(db_column='promo_descripcion', max_length=50)),
                ('promocionEstado', models.BooleanField(db_column='promo_estado', default=True)),
            ],
            options={
                'verbose_name': 'Promocion',
                'verbose_name_plural': 'Promociones',
                'db_table': 't_promocion',
            },
        ),
        migrations.CreateModel(
            name='RazaModel',
            fields=[
                ('razaId', models.AutoField(auto_created=True, db_column='raza_id', help_text='Aqui va el id', primary_key=True, serialize=False, unique=True, verbose_name='ID de la raza')),
                ('razaNombre', models.CharField(db_column='raza_nombre', max_length=45, verbose_name='Nombre de la raza')),
            ],
            options={
                'db_table': 't_raza',
            },
        ),
        migrations.CreateModel(
            name='TipoModel',
            fields=[
                ('tipoId', models.AutoField(db_column='tipo_id', primary_key=True, serialize=False, unique=True)),
                ('tipoNombre', models.CharField(db_column='tipo_nombre', max_length=45)),
                ('raza', models.ForeignKey(db_column='raza_id', help_text='Id de la raza', on_delete=django.db.models.deletion.PROTECT, related_name='tiposraza', to='administracion.razamodel', verbose_name='Raza')),
            ],
            options={
                'verbose_name': 'Tipo',
                'verbose_name_plural': 'Tipos',
                'db_table': 't_tipo',
            },
        ),
        migrations.CreateModel(
            name='MascotaModel',
            fields=[
                ('mascotaId', models.AutoField(db_column='mascota_id', primary_key=True, serialize=False, unique=True)),
                ('mascotaNombre', models.CharField(db_column='mascota_nombre', max_length=45)),
                ('mascotaFechaNacimiento', models.DateField(db_column='mascota_fecnac')),
                ('mascotaSexo', models.CharField(choices=[('M', 'Macho'), ('H', 'Hembra')], db_column='mascota_sexo', default='M', max_length=1)),
                ('cliente', models.ForeignKey(db_column='cli_dni', on_delete=django.db.models.deletion.PROTECT, related_name='mascotasCliente', to='administracion.clientemodel')),
                ('tipo', models.ForeignKey(db_column='tipo_id', on_delete=django.db.models.deletion.PROTECT, related_name='mascotasTipo', to='administracion.tipomodel')),
            ],
            options={
                'verbose_name': 'Mascota',
                'verbose_name_plural': 'Mascotas',
                'db_table': 't_mascota',
            },
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('historialId', models.AutoField(db_column='historial_id', primary_key=True, serialize=False, unique=True)),
                ('historialCanje', models.BooleanField(db_column='historial_canje', default=True)),
                ('mascota', models.ForeignKey(db_column='mascota_id', on_delete=django.db.models.deletion.PROTECT, related_name='historialesMascota', to='administracion.mascotamodel')),
                ('promocion', models.ForeignKey(db_column='promo_id', on_delete=django.db.models.deletion.PROTECT, related_name='historialesPromocion', to='administracion.promocionmodel')),
            ],
            options={
                'verbose_name': 'Historial',
                'verbose_name_plural': 'Historiales',
                'db_table': 't_historial',
            },
        ),
    ]
