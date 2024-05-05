from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class BaseModel(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def set_created_at_and_updated_at(sender, instance, **kwargs):
    if instance._state.adding:
        instance.createdAt = timezone.now()
    else:
        instance.updatedAt = timezone.now()


@receiver(pre_save)
def pre_save_handler(sender, instance, **kwargs):
    if issubclass(sender, BaseModel):
        set_created_at_and_updated_at(sender, instance, **kwargs)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo de correo electrónico es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.FileField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # Agrega otros campos personalizados según tus necesidades

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'User'
        swappable = 'AUTH_USER_MODEL'
        permissions = (('can_add_something', 'Can add something'),)  # ejemplo de permiso
        default_permissions = ()


class Provincias(BaseModel):
    provincia = models.CharField(max_length=250)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.provincia
    
class Municipios(BaseModel):
    provincia = models.ForeignKey('Provincias',on_delete=models.CASCADE)
    municipio = models.CharField(max_length=250)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.municipio
    

class TipoSectores(BaseModel):
    tipoSector = models.CharField( max_length=250)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.tipoSector
    

class Sectores(BaseModel):
    tipoSector = models.ForeignKey('TipoSectores',on_delete=models.CASCADE)
    sector = models.CharField( max_length=250)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.sector
    
    
class Especies(BaseModel):
    codigo = models.PositiveIntegerField()
    especies = models.CharField(max_length=250)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.especies
    
class Enfermedades(BaseModel):
    idenfermedad = models.PositiveIntegerField() 
    enfermedad = models.CharField(max_length=250) 
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.enfermedad
    
class Propietarios(BaseModel):
    propietario = models.CharField( max_length=20)
    sector = models.ForeignKey('Sectores',on_delete=models.CASCADE)
    municipio = models.ForeignKey('Municipios',on_delete=models.CASCADE)
    provincia = models.ForeignKey('Provincias',on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.propietario
    
class Unidad(BaseModel):
    nombre = models.CharField(max_length = 250)
    provincia_uni = models.ForeignKey("Provincias",on_delete=models.CASCADE,related_name ='provincia_uni')
    municipio_uni = models.ForeignKey("Municipios",on_delete=models.CASCADE,related_name ='municipio_uni')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class NotiDiaria(BaseModel):
    no_orden = models.IntegerField()
    municipio = models.ForeignKey("Municipios", on_delete=models.CASCADE, db_column='municipio')
    unidad = models.ForeignKey("Unidad", on_delete=models.CASCADE)
    propietario = models.ForeignKey("Propietarios", on_delete=models.CASCADE, db_column='propietario')
    codigo_entidad = models.IntegerField()
    codigo_especialista = models.IntegerField()
    poblacion = models.IntegerField(null=True, blank=True)
    enfermos = models.IntegerField(null=True, blank=True)
    muertos = models.IntegerField(null=True, blank=True)
    sacrificados = models.IntegerField(null=True, blank=True)
    fecha_confeccion = models.DateField(auto_now=False, auto_now_add=False)
    fecha_confirmacion = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    fecha_cierre = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    esta_activo = models.BooleanField()
    latitud = models.DecimalField(max_digits=20, decimal_places=14)
    longitud = models.DecimalField(max_digits=20, decimal_places=14)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class Seguimientos(BaseModel):
    provincia = models.ForeignKey("Provincias", on_delete=models.CASCADE)
    numOrden = models.IntegerField()
    enfermos = models.IntegerField()
    muertos = models.IntegerField()
    sacrificados = models.IntegerField()
    recuperados = models.IntegerField()
    observaciones = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class Letalidad(BaseModel):
    enfermedad = models.ManyToManyField("Enfermedades")
    nuevosBrotes = models.IntegerField()
    nuevosEnfermos = models.IntegerField()
    muertos = models.IntegerField()
    sacrificados = models.IntegerField()
    tratados = models.IntegerField()
    vacunados = models.IntegerField()
    centroInformante = models.CharField(max_length=50)
    fecha = models.DateField(auto_now_add=True)
    sector = models.ForeignKey("Sectores", on_delete=models.CASCADE)
    municipio = models.ForeignKey("Municipios", on_delete=models.CASCADE)
    provincia = models.ForeignKey("Provincias", on_delete=models.CASCADE)
    especie = models.ForeignKey("Especies", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class Traslado(BaseModel):
    fecha = models.DateField(auto_now_add=True)
    provincia = models.ForeignKey("Provincias", on_delete=models.CASCADE)
    municipio = models.ForeignKey("Municipios", on_delete=models.CASCADE)
    propietario = models.ForeignKey("Propietarios", on_delete=models.CASCADE)
    tipoAnimal = models.CharField(max_length=50)
    investigaciones = models.TextField(max_length=500)
    provinciaDestino = models.CharField(max_length=50)
    municipioDestino = models.CharField(max_length=50)
    propietarioDestino = models.CharField(max_length=50)
    solicita = models.CharField(max_length=100)
    tramita = models.CharField(max_length=100)
    autoriza = models.CharField(max_length=100)
    nacion = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)



