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

    class Meta:
        model = Sectores
        fields = '__all__'
        

class PropietariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propietarios
        fields = '__all__'


class EspeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especies
        fields = '__all__'

class EnfermedadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfermedades
        fields = '__all__'

class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = '__all__'

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
    class Meta:
        model = Seguimientos
        fields = '__all__'


class LetalidadSerializer(serializers.ModelSerializer):
    enfermedad = EnfermedadesSerializer(many=True)
    sector = serializers.PrimaryKeyRelatedField(queryset=Sectores.objects.all())
    municipio = serializers.PrimaryKeyRelatedField(queryset=Municipios.objects.all())
    provincia = serializers.PrimaryKeyRelatedField(queryset=Provincias.objects.all())
    especie = serializers.PrimaryKeyRelatedField(queryset=Especies.objects.all())

    class Meta:
        model = Letalidad
        fields = '__all__'

    def create(self, validated_data):
        enfermedades_data = validated_data.pop('enfermedad', None)
        letalidad = Letalidad.objects.create(**validated_data)
        if enfermedades_data:
            for enfermedad_data in enfermedades_data:
                enfermedad_obj, _ = Enfermedades.objects.get_or_create(**enfermedad_data)
                letalidad.enfermedad.add(enfermedad_obj)
        return letalidad

    def update(self, instance, validated_data):
        # Actualizamos los campos de la instancia
        instance.nuevosBrotes = validated_data.get('nuevosBrotes', instance.nuevosBrotes)
        instance.nuevosEnfermos = validated_data.get('nuevosEnfermos', instance.nuevosEnfermos)
        instance.muertos = validated_data.get('muertos', instance.muertos)
        instance.sacrificados = validated_data.get('sacrificados', instance.sacrificados)
        instance.tratados = validated_data.get('tratados', instance.tratados)
        instance.vacunados = validated_data.get('vacunados', instance.vacunados)
        instance.centroInformante = validated_data.get('centroInformante', instance.centroInformante)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.sector = validated_data.get('sector', instance.sector)
        instance.municipio = validated_data.get('municipio', instance.municipio)
        instance.provincia = validated_data.get('provincia', instance.provincia)
        instance.especie = validated_data.get('especie', instance.especie)

        # Actualizamos las enfermedades asociadas
        if 'enfermedad' in validated_data:
            instance.enfermedad.clear()  # Limpiamos las enfermedades actuales
            enfermedades_data = validated_data.pop('enfermedad')
            for enfermedad_data in enfermedades_data:
                enfermedad_obj, _ = Enfermedades.objects.get_or_create(**enfermedad_data)
                instance.enfermedad.add(enfermedad_obj)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['municipio'] = MunicipiosSerializer(instance.municipio).data
        representation['sector'] = SectoresSerializer(instance.sector).data
        representation['provincia'] = ProvinciasSerializer(instance.provincia).data
        representation['especie'] = EspeciesSerializer(instance.especie).data
        representation['enfermedad'] = EnfermedadesSerializer(instance.enfermedad.all(), many=True).data
        return representation
    
    
class TrasladoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traslado
        fields = '__all__'
