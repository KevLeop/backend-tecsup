# Generated by Django 3.1.7 on 2021-03-18 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0003_auto_20210318_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especiemodel',
            name='especieNombre',
            field=models.CharField(db_column='especie_nombre', max_length=45, unique=True, verbose_name='Nombre de la especie'),
        ),
        migrations.AlterField(
            model_name='razamodel',
            name='especie',
            field=models.ForeignKey(db_column='especie_id', help_text='Id de la Especie', on_delete=django.db.models.deletion.PROTECT, related_name='tiposespecie', to='administracion.especiemodel', verbose_name='Especie'),
        ),
    ]