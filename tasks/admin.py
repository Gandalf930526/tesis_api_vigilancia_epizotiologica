from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.
# admin.site.register(BaseModel)
#admin.site.register(CustomUserManager)
admin.site.register(User,UserAdmin)
admin.site.register(Municipios)
admin.site.register(Provincias)
admin.site.register(Propietarios)
admin.site.register(Sectores)
admin.site.register(TipoSectores)
admin.site.register(Especies)
admin.site.register(Enfermedades)
admin.site.register(NotiDiaria)
admin.site.register(Seguimientos)
admin.site.register(Letalidad)
admin.site.register(Traslado)