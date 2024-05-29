from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh_token = self.get_token(self.user)

        # Agrega los datos adicionales del usuario en la respuesta
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            # Agrega otros campos adicionales que desees incluir en la respuesta
        }

        data['refresh_token'] = str(refresh_token)
        data['access_token'] = str(refresh_token.access_token)

        return data
    
class ProvinciasSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Provincias
        fields = '__all__'


class MunicipiosSerializer(serializers.ModelSerializer):
    provincia = serializers.PrimaryKeyRelatedField(queryset=Provincias.objects.all())

    class Meta:
        model = Municipios
        fields = '__all__'

    def to_internal_value(self, data):
        provincia_data = data.get('provincia')
        if isinstance(provincia_data, dict):
            provincia_id = provincia_data.get('id')
            provincia = Provincias.objects.get(pk=provincia_id)
            data['provincia'] = provincia.id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['provincia'] = ProvinciasSerializer(instance.provincia).data
        return ret


class TipoSectoresSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TipoSectores
        fields = '__all__'


class SectoresSerializer(serializers.ModelSerializer):
    tipoSector = serializers.PrimaryKeyRelatedField(queryset=TipoSectores.objects.all())
    
    class Meta:
        model = Sectores
        fields = '__all__'
        
    def to_internal_value(self, data):
        tipoSector_data = data.get('tipoSector')
        if isinstance(tipoSector_data, dict):
            tipoSector_id = tipoSector_data.get('id')
            tipoSector = TipoSectores.objects.get(pk=tipoSector_id)
            data['tipoSector'] = tipoSector.id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['tipoSector'] = TipoSectoresSerializer(instance.tipoSector).data
        return ret       
    
        

class PropietariosSerializer(serializers.ModelSerializer):
    sector = serializers.PrimaryKeyRelatedField(queryset=Sectores.objects.all())
    municipio = serializers.PrimaryKeyRelatedField(queryset=Municipios.objects.all())
    provincia = serializers.PrimaryKeyRelatedField(queryset=Provincias.objects.all())
    
    class Meta:
        model = Propietarios
        fields = '__all__'
    
    def to_internal_value(self, data):
        sector_data = data.get('sector')
        municipio_data = data.get('municipio') 
        provincia_data = data.get('provincia')
        if isinstance(sector_data, dict):
            sector_id = sector_data.get('id')
            sector = Sectores.objects.get(pk=sector_id)
            data['sector'] = sector.id
        
        if isinstance(municipio_data, dict):
            municipio_id = municipio_data.get('id')
            municipio = Municipios.objects.get(pk=municipio_id)
            data['municipio'] = municipio.id            
        
        if isinstance(provincia_data, dict):
            provincia_id = provincia_data.get('id')
            provincia = Provincias.objects.get(pk=provincia_id)
            data['provincia'] = provincia.id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['sector'] = SectoresSerializer(instance.sector).data
        ret['municipio'] = MunicipiosSerializer(instance.municipio).data       
        ret['provincia'] = ProvinciasSerializer(instance.provincia).data
        return ret    
  
class EspeciesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Especies
        fields = '__all__'

class EnfermedadesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Enfermedades
        fields = '__all__'

class UnidadSerializer(serializers.ModelSerializer):
    municipio_uni = serializers.PrimaryKeyRelatedField(queryset=Municipios.objects.all())
    provincia_uni = serializers.PrimaryKeyRelatedField(queryset=Provincias.objects.all())
        
    class Meta:
        model = Unidad
        fields = '__all__'
        
    def to_internal_value(self, data):
        municipio_data = data.get('municipio_uni') 
        provincia_data = data.get('provincia_uni')
        
        if isinstance(municipio_data, dict):
            municipio_id = municipio_data.get('id')
            municipio = Municipios.objects.get(pk=municipio_id)
            data['municipio_uni'] = municipio.id            
        
        if isinstance(provincia_data, dict):
            provincia_id = provincia_data.get('id')
            provincia = Provincias.objects.get(pk=provincia_id)
            data['provincia_uni'] = provincia.id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['municipio_uni'] = MunicipiosSerializer(instance.municipio_uni).data       
        ret['provincia_uni'] = ProvinciasSerializer(instance.provincia_uni).data
        return ret      

class NotiDiariaSerializer(serializers.ModelSerializer):
    municipio = serializers.PrimaryKeyRelatedField(queryset=Municipios.objects.all())
    unidad = serializers.PrimaryKeyRelatedField(queryset=Unidad.objects.all())
    propietario = serializers.PrimaryKeyRelatedField(queryset=Propietarios.objects.all())

    class Meta:
        model = NotiDiaria
        fields = "__all__"

    def to_internal_value(self, data):
        municipio_data = data.get('municipio')
        unidad_data = data.get('unidad')
        propietario_data = data.get('propietario')
        if isinstance(municipio_data, dict):
            municipio_id = municipio_data.get('id')
            municipio = Municipios.objects.get(pk=municipio_id)
            data['municipio'] = municipio.id
        if isinstance(unidad_data, dict):
            unidad_id = unidad_data.get('id')
            unidad = Unidad.objects.get(pk=unidad_id)
            data['unidad'] = unidad.id
        if isinstance(propietario_data, dict):
            propietario_id = propietario_data.get('id')
            propietario = Propietarios.objects.get(pk=propietario_id)
            data['propietario'] = propietario.id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['municipio'] = MunicipiosSerializer(instance.municipio).data
        ret['unidad'] = UnidadSerializer(instance.unidad).data
        ret['propietario'] = PropietariosSerializer(instance.propietario).data
        return ret

class SeguimientosSerializer(serializers.ModelSerializer):
    provincia = serializers.PrimaryKeyRelatedField(queryset=Provincias.objects.all())
    
    class Meta:
        model = Seguimientos
        fields = '__all__'
        
    def to_internal_value(self, data):
        provincia_data = data.get('provincia')
        if isinstance(provincia_data, dict):
            provincia_id = provincia_data.get('id')
            provincia = Provincias.objects.get(pk=provincia_id)
            data['provincia'] = provincia.id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['provincia'] = ProvinciasSerializer(instance.provincia).data
        return ret  


class LetalidadSerializer(serializers.ModelSerializer):
    enfermedad = serializers.PrimaryKeyRelatedField(queryset=Enfermedades.objects.all())
    sector = serializers.PrimaryKeyRelatedField(queryset=Sectores.objects.all())
    municipio = serializers.PrimaryKeyRelatedField(queryset=Municipios.objects.all())
    provincia = serializers.PrimaryKeyRelatedField(queryset=Provincias.objects.all())
    especie = serializers.PrimaryKeyRelatedField(queryset=Especies.objects.all())

    class Meta:
        model = Letalidad
        fields = '__all__'

    def to_internal_value(self, data):
        municipio_data = data.get('municipio')
        sector_data = data.get('sector')
        enfermedad_data = data.get('enfermedad')
        provincia_data = data.get('provincia')
        especie_data = data.get('especie')
        if isinstance(municipio_data, dict):
            municipio_id = municipio_data.get('id')
            municipio = Municipios.objects.get(pk=municipio_id)
            data['municipio'] = municipio.id
        if isinstance(sector_data, dict):
            sector_id = sector_data.get('id')
            sector = Sectores.objects.get(pk=sector_id)
            data['sector'] = sector.id
        if isinstance(enfermedad_data, dict):
            enfermedad_id = enfermedad_data.get('id')
            enfermedad = Enfermedades.objects.get(pk=enfermedad_id)
            data['enfermedad'] = enfermedad.id
        if isinstance(provincia_data, dict):
            provincia_id = provincia_data.get('id')
            provincia = Provincias.objects.get(pk=provincia_id)
            data['provincia'] = provincia.id
        if isinstance(especie_data, dict):
            especie_id = especie_data.get('id')
            especie = Especies.objects.get(pk=especie_id)
            data['especie'] = especie.id    
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['municipio'] = MunicipiosSerializer(instance.municipio).data
        representation['sector'] = SectoresSerializer(instance.sector).data
        representation['provincia'] = ProvinciasSerializer(instance.provincia).data
        representation['especie'] = EspeciesSerializer(instance.especie).data
        representation['enfermedad'] = EnfermedadesSerializer(instance.enfermedad).data
        return representation
    
    
class TrasladoSerializer(serializers.ModelSerializer):
    provincia = serializers.PrimaryKeyRelatedField(queryset=Provincias.objects.all())
    municipio = serializers.PrimaryKeyRelatedField(queryset=Municipios.objects.all())
    propietario = serializers.PrimaryKeyRelatedField(queryset=Propietarios.objects.all())
    
    class Meta:
        model = Traslado
        fields = '__all__'
    
    def to_internal_value(self, data):
        provincia_data = data.get('provincia')
        municipio_data = data.get('municipio')
        propietario_data = data.get('propietario')
        if isinstance(provincia_data, dict):
            provincia_id = provincia_data.get('id')
            provincia = Provincias.objects.get(pk=provincia_id)
            data['provincia'] = provincia.id
        if isinstance(municipio_data, dict):
            municipio_id = municipio_data.get('id')
            municipio = Municipios.objects.get(pk=municipio_id)
            data['municipio'] = municipio.id     
        if isinstance(propietario_data, dict):
            propietario_id = propietario_data.get('id')
            propietario = Propietarios.objects.get(pk=propietario_id)
            data['propietario'] = propietario.id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['provincia'] = ProvinciasSerializer(instance.provincia).data
        ret['municipio'] = MunicipiosSerializer(instance.municipio).data
        ret['propietario'] = PropietariosSerializer(instance.propietario).data
        return ret    
    
