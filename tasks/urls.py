from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from tasks import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tasks.views import CustomTokenObtainPairView, UserRegistrationView


routers = routers.DefaultRouter()
routers.register(r'municipios', views.MunicipiosView, 'municipios')
routers.register(r'provincias', views.ProvinciasView, 'provincias')
routers.register(r'propietarios', views.PropietariosView, 'propietarios')
routers.register(r'sectores', views.SectoresView, 'sectores')
routers.register(r'tipoSectores', views.TipoSectoresView, 'tipoSectores')
routers.register(r'especies', views.EspeciesView, 'especies')
routers.register(r'enfermedades', views.EnfermedadesView, 'enfermedades')
routers.register(r'unidad', views.UnidadView, 'unidad')
routers.register(r'notiDiaria', views.NotiDiariaView, 'notiDiaria')
routers.register(r'seguimientos', views.SeguimientosView, 'seguimientos')
routers.register(r'letalidadCanina', views.LetalidadCaninaView, 'letalidadCanina')
routers.register(r'traslado', views.TrasladoView, 'traslado')




urlpatterns = [
    path("", include(routers.urls)),
    path("docs/", include_docs_urls(title = 'API VETERINARIA')),
    path('api/v1/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/register/', UserRegistrationView.as_view(), name='user-register'),
]