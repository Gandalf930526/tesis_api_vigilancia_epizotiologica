from rest_framework import viewsets
from .serializer import *
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
            'status': status.HTTP_201_CREATED,
            'message': 'Registro exitoso',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Agrega un mensaje personalizado y el código de estado en caso de éxito
            data['message'] = 'Inicio de sesión exitoso'
            data['status'] = status.HTTP_200_OK
        else:
            # Agrega un mensaje personalizado y el código de estado en caso de error
            data['message'] = 'Credenciales de inicio de sesión incorrectas'
            data['status'] = status.HTTP_400_BAD_REQUEST

        return Response(data)


class MunicipiosView(viewsets.ModelViewSet):
    serializer_class = MunicipiosSerializer
    queryset = Municipios.objects.all()

class ProvinciasView(viewsets.ModelViewSet):
    serializer_class = ProvinciasSerializer
    queryset = Provincias.objects.all()

class PropietariosView(viewsets.ModelViewSet):
    serializer_class = PropietariosSerializer
    queryset = Propietarios.objects.all()

class SectoresView(viewsets.ModelViewSet):
    serializer_class = SectoresSerializer
    queryset = Sectores.objects.all()

class TipoSectoresView(viewsets.ModelViewSet):
    serializer_class = TipoSectoresSerializer
    queryset = TipoSectores.objects.all()

class EspeciesView(viewsets.ModelViewSet):
    serializer_class = EspeciesSerializer
    queryset = Especies.objects.all()

class EnfermedadesView(viewsets.ModelViewSet):
    serializer_class = EnfermedadesSerializer
    queryset = Enfermedades.objects.all()

class UnidadView(viewsets.ModelViewSet):
    serializer_class = UnidadSerializer
    queryset = Unidad.objects.all()

class NotiDiariaView(viewsets.ModelViewSet):
    serializer_class = NotiDiariaSerializer
    queryset = NotiDiaria.objects.all()

class SeguimientosView(viewsets.ModelViewSet):
    serializer_class = SeguimientosSerializer
    queryset = Seguimientos.objects.all()

class LetalidadCaninaView(viewsets.ModelViewSet):
    serializer_class = LetalidadCaninaSerializer
    queryset = LetalidadCanina.objects.all()

class TrasladoView(viewsets.ModelViewSet):
    serializer_class = TrasladoSerializer
    queryset = Traslado.objects.all()