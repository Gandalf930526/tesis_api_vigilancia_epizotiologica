from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


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

class MunicipiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipios
        #fields = ('id', 'title', 'description', 'done')
        fields = '__all__'

class ProvinciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincias
        #fields = ('id','codigo', 'nombre')
        fields = '__all__'

class PropietariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propietarios
        #fields = ('id','codigo', 'nombre')
        fields = '__all__'

class SectoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sectores
        #fields = ('id','codigo', 'nombre')
        fields = '__all__'

class TipoSectoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSectores
        #fields = ('id','codigo', 'nombre')
        fields = '__all__'

class EspeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especies
        #fields = ('id','codigo', 'nombre')
        fields = '__all__'

class EnfermedadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfermedades
        #fields = ('id','codigo', 'nombre')
        fields = '__all__'

class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = '__all__'



class NotiDiariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotiDiaria
        fields = "__all__"

class SeguimientosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimientos
        fields = '__all__'

class LetalidadCaninaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LetalidadCanina
        fields = '__all__'

class TrasladoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traslado
        fields = '__all__'



