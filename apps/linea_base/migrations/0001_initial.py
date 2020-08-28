# Generated by Django 3.0.7 on 2020-08-20 01:21

import apps.linea_base.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fase', '0001_initial'),
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineaBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador', models.CharField(default=apps.linea_base.models.random_id, editable=False, max_length=9)),
                ('descripcion', models.TextField(default=None, null=True)),
                ('fecha_creacion', models.DateField(default=datetime.date.today)),
                ('estado', models.CharField(choices=[('Abierta', 'Abierta'), ('Cerrada', 'Cerrada'), ('Rota', 'Rota')], default='Abierta', max_length=30)),
                ('fase', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='fase.Fase')),
                ('items', models.ManyToManyField(blank=True, related_name='LineaBase', to='item.Item')),
            ],
            options={
                'permissions': [('crear_linea_base', 'crear_linea_base'), ('cerrar_linea_base', 'cerrar_linea_base'), ('ver_linea_base', 'ver_linea_base'), ('editar_linea_base', 'editar_linea_base'), ('agregar_item_linea_base', 'agregar_item_linea_base'), ('quitar_item_linea_base', 'quitar_item_linea_base'), ('listar_item_linea_base', 'listar_item_linea_base'), ('estado_linea_base', 'estado_linea_base')],
                'default_permissions': (),
            },
        ),
    ]