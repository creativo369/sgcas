# Generated by Django 3.0.5 on 2020-04-25 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comite', '0001_initial'),
        ('proyecto', '0004_auto_20200425_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='comite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='comite.Comite'),
        ),
    ]