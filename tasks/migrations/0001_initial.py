# Generated by Django 5.0.4 on 2024-05-05 19:43

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enfermedades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idenfermedad', models.PositiveIntegerField()),
                ('enfermedad', models.CharField(max_length=250)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Especies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.PositiveIntegerField()),
                ('especies', models.CharField(max_length=250)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Municipios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('municipio', models.CharField(max_length=250)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Provincias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provincia', models.CharField(max_length=250)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sectores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.CharField(max_length=250)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TipoSectores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoSector', models.CharField(max_length=250)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('avatar', models.FileField(blank=True, null=True, upload_to='')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'User',
                'permissions': (('can_add_something', 'Can add something'),),
                'swappable': 'AUTH_USER_MODEL',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Propietarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propietario', models.CharField(max_length=20)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.municipios')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.provincias')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.sectores')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='municipios',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.provincias'),
        ),
        migrations.CreateModel(
            name='Letalidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nuevosBrotes', models.IntegerField()),
                ('nuevosEnfermos', models.IntegerField()),
                ('muertos', models.IntegerField()),
                ('sacrificados', models.IntegerField()),
                ('tratados', models.IntegerField()),
                ('vacunados', models.IntegerField()),
                ('centroInformante', models.CharField(max_length=50)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('enfermedad', models.ManyToManyField(to='tasks.enfermedades')),
                ('especie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.especies')),
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.municipios')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.provincias')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.sectores')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Seguimientos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numOrden', models.IntegerField()),
                ('enfermos', models.IntegerField()),
                ('muertos', models.IntegerField()),
                ('sacrificados', models.IntegerField()),
                ('recuperados', models.IntegerField()),
                ('observaciones', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.provincias')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='sectores',
            name='tipoSector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.tiposectores'),
        ),
        migrations.CreateModel(
            name='Traslado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('tipoAnimal', models.CharField(max_length=50)),
                ('investigaciones', models.TextField(max_length=500)),
                ('provinciaDestino', models.CharField(max_length=50)),
                ('municipioDestino', models.CharField(max_length=50)),
                ('propietarioDestino', models.CharField(max_length=50)),
                ('solicita', models.CharField(max_length=100)),
                ('tramita', models.CharField(max_length=100)),
                ('autoriza', models.CharField(max_length=100)),
                ('nacion', models.CharField(max_length=100)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.municipios')),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.propietarios')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.provincias')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Unidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('municipio_uni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipio_uni', to='tasks.municipios')),
                ('provincia_uni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provincia_uni', to='tasks.provincias')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NotiDiaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_orden', models.IntegerField()),
                ('codigo_entidad', models.IntegerField()),
                ('codigo_especialista', models.IntegerField()),
                ('poblacion', models.IntegerField(blank=True, null=True)),
                ('enfermos', models.IntegerField(blank=True, null=True)),
                ('muertos', models.IntegerField(blank=True, null=True)),
                ('sacrificados', models.IntegerField(blank=True, null=True)),
                ('fecha_confeccion', models.DateField()),
                ('fecha_confirmacion', models.DateField(blank=True, null=True)),
                ('fecha_cierre', models.DateField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('esta_activo', models.BooleanField()),
                ('latitud', models.DecimalField(decimal_places=14, max_digits=20)),
                ('longitud', models.DecimalField(decimal_places=14, max_digits=20)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('municipio', models.ForeignKey(db_column='municipio', on_delete=django.db.models.deletion.CASCADE, to='tasks.municipios')),
                ('propietario', models.ForeignKey(db_column='propietario', on_delete=django.db.models.deletion.CASCADE, to='tasks.propietarios')),
                ('unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.unidad')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
