# Generated by Django 4.2.2 on 2023-12-28 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Interés',
                'verbose_name_plural': 'Intereses',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='users/perfil-del-usuario.png', upload_to='users/')),
                ('gender', models.CharField(blank=True, choices=[('F', 'Femenino'), ('M', 'Masculino'), ('NB', 'No binario'), ('O', 'Otro')], max_length=20, null=True, verbose_name='Género')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('location', models.CharField(blank=True, max_length=80, null=True)),
                ('bio', models.TextField(blank=True, max_length=400, null=True)),
                ('interests', models.ManyToManyField(to='accounts.interest', verbose_name='Intereses')),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
                'ordering': ['-id'],
            },
        ),
    ]