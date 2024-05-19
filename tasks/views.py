from rest_framework import viewsets
from .serializer import *
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, fields
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import numpy as np 
from scipy.stats import poisson

# Create your views here.
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

class ProvinciasView(viewsets.ModelViewSet):
    serializer_class = ProvinciasSerializer
    queryset = Provincias.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class PropietariosView(viewsets.ModelViewSet):
    serializer_class = PropietariosSerializer
    queryset = Propietarios.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class SectoresView(viewsets.ModelViewSet):
    serializer_class = SectoresSerializer
    queryset = Sectores.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class TipoSectoresView(viewsets.ModelViewSet):
    serializer_class = TipoSectoresSerializer
    queryset = TipoSectores.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class EspeciesView(viewsets.ModelViewSet):
    serializer_class = EspeciesSerializer
    queryset = Especies.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class EnfermedadesView(viewsets.ModelViewSet):
    serializer_class = EnfermedadesSerializer
    queryset = Enfermedades.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class UnidadView(viewsets.ModelViewSet):
    serializer_class = UnidadSerializer
    queryset = Unidad.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class NotiDiariaView(viewsets.ModelViewSet):
    serializer_class = NotiDiariaSerializer
    queryset = NotiDiaria.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class SeguimientosView(viewsets.ModelViewSet):
    serializer_class = SeguimientosSerializer
    queryset = Seguimientos.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class LetalidadView(viewsets.ModelViewSet):
    serializer_class = LetalidadSerializer
    queryset = Letalidad.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class TrasladoView(viewsets.ModelViewSet):
    serializer_class = TrasladoSerializer
    queryset = Traslado.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class LetalidadPorMunicipio(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            municipio_id = request.query_params.get('municipio_id')
            fecha_inicio = request.query_params.get('fecha_inicio')
            fecha_fin = request.query_params.get('fecha_fin')
            especie_id = request.query_params.get('especie_id')

            if not (municipio_id and fecha_inicio and fecha_fin and especie_id):
                return Response({"status": "error", "message": "Los parámetros municipio_id, fecha_inicio, fecha_fin y especie son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener instancias de los objetos de Municipio y Especie
            letalidades = Letalidad.objects.filter(municipio_id=municipio_id, fecha__range=[fecha_inicio, fecha_fin], especie_id=especie_id)

            if not letalidades.exists():
                return Response({"status": "error", "message": "No existe letalidad para esos parámetros"}, status=status.HTTP_204_NO_CONTENT)
            
            # Serializar los objetos de Letalidad
            serializer = LetalidadSerializer(letalidades, many=True)

            # Diccionario para almacenar los resultados agrupados
            resultados_agrupados = {}

            # Agrupación y suma de los nuevos parámetros
            for letalidad in serializer.data:
                key = (
                        letalidad['enfermedad']['id'], 
                        letalidad['especie']['id'], 
                        letalidad['municipio']['id'],  
                        letalidad['provincia']['id'],  
                        letalidad['sector']['id'],     
                        letalidad['centroInformante']
                )
        
                if key not in resultados_agrupados:
                    resultados_agrupados[key] = {
                        'enfermedad': letalidad['enfermedad'],
                        'especie': letalidad['especie'],
                        'municipio': letalidad['municipio'],
                        'provincia': letalidad['provincia'],
                        'sector': letalidad['sector'],
                        'centroInformante': letalidad['centroInformante'],
                        'nuevosBrotes': 0,
                        'nuevosEnfermos': 0,
                        'muertos': 0,
                        'sacrificados': 0,
                        'tratados': 0,
                        'vacunados': 0
                    }
                resultados_agrupados[key]['nuevosBrotes'] += letalidad['nuevosBrotes']
                resultados_agrupados[key]['nuevosEnfermos'] += letalidad['nuevosEnfermos']
                resultados_agrupados[key]['muertos'] += letalidad['muertos']
                resultados_agrupados[key]['sacrificados'] += letalidad['sacrificados']
                resultados_agrupados[key]['tratados'] += letalidad['tratados']
                resultados_agrupados[key]['vacunados'] += letalidad['vacunados']
        
            # Convertir el diccionario a una lista para la serialización
            resultados_agrupados_list = list(resultados_agrupados.values())

            # Serializar los resultados agrupados
            grouped_serializer = LetalidadSerializer(data=resultados_agrupados_list, many=True)
            grouped_serializer.is_valid(raise_exception=True)

            for data in grouped_serializer.validated_data:
                    data['municipio'] = MunicipiosSerializer(Municipios.objects.get(id=data['municipio'].id)).data
                    data['sector'] = SectoresSerializer(Sectores.objects.get(id=data['sector'].id)).data
                    data['provincia'] = ProvinciasSerializer(Provincias.objects.get(id=data['provincia'].id)).data
                    data['especie'] = EspeciesSerializer(Especies.objects.get(id=data['especie'].id)).data
                    data['enfermedad'] = EnfermedadesSerializer(Enfermedades.objects.get(id=data['enfermedad'].id)).data
                    total_animales_enfermos = data['nuevosEnfermos'] + data['tratados']
                    data['letalidad'] = (data['muertos'] / total_animales_enfermos) if total_animales_enfermos != 0 else 0
            
            # Mensaje de éxito
            return Response({"status": "success", "message": "La petición fue exitosa", "data": grouped_serializer.validated_data})
        
        except ObjectDoesNotExist:
            # Manejo de error cuando no hay letalidad para los parámetros dados
            return Response({"status": "error", "message": "No existe letalidad para esos parámetros"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # Manejo de errores generales
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PoissonMap(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def calcular_probabilidad_poisson(matriz, tasa_media):
        # Inicializar una matriz para almacenar las probabilidades calculadas
        probabilidades_poisson = np.zeros_like(matriz, dtype=float)

        # Calcular la probabilidad de Poisson para cada elemento de la matriz
        for i in range(matriz.shape[0]):
            for j in range(matriz.shape[1]):
                num_eventos = matriz[i][j]
                probabilidades_poisson[i][j] = poisson.pmf(num_eventos, tasa_media)

        return probabilidades_poisson

    def get(self, request):
        try:
            municipio_id = request.query_params.get('municipio_id')
            fecha_inicio = request.query_params.get('fecha_inicio')
            fecha_fin = request.query_params.get('fecha_fin')
            activo = request.query_params.get('activo')

            if not (fecha_inicio and fecha_fin and activo):
                return Response({"status": "error", "message": "Los parámetros fecha_inicio, fecha_fin, activo, municipio_id son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener instancias de los objetos de NotiDiaria
            notiDiaria = NotiDiaria.objects.filter(fecha_confirmacion__range=[fecha_inicio, fecha_fin], esta_activo=activo, municipio=municipio_id)
            print(notiDiaria);
            if not notiDiaria.exists():
                return Response({"status": "error", "message": "No hay datos para esos parámetros"}, status=status.HTTP_204_NO_CONTENT)

            # Calcular la tasa media
            muertos_total = sum(noti.muertos for noti in notiDiaria)
            num_notiDiaria = notiDiaria.count()
            tasa_media = muertos_total / num_notiDiaria

            # Crear matriz de muertos
            matriz_muertos = np.array([[noti.muertos] for noti in notiDiaria])

            # Calcular probabilidades de Poisson
            probabilidades_poisson = self.calcular_probabilidad_poisson(matriz_muertos, tasa_media)

            # Calcular cuartiles
            q1 = np.percentile(probabilidades_poisson, 25)
            q2 = np.percentile(probabilidades_poisson, 50)
            q3 = np.percentile(probabilidades_poisson, 75)

            # Serializar los datos
            serializer = NotiDiariaSerializer(notiDiaria, many=True)

            # Agregar resultados de cálculos a cada instancia serializada
            serialized_data = serializer.data
            for idx, instance_data in enumerate(serialized_data):
                instance_data["probabilidad_poisson"] = probabilidades_poisson[idx][0]
                instance_data["q1"] = q1
                instance_data["q2"] = q2
                instance_data["q3"] = q3

            # Mensaje de éxito con los datos calculados
            return Response({"status": "success", "message": "La petición fue exitosa", "data": serialized_data})

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)