#definir todas las urls que va a usar la aplicacion gestionEmpleados
from django.urls import path
from . import views
"""

"""
urlpatterns=[
    path('', views.index, name='index'),
    path('crear_usuario/',views.crear_usuario,name='crear_usuario'),
    path('login/',views.login,name='login'),
    path('login/geolocalizacion/',views.geolocalizacion,name='geolocalizacion'),
    path('login/asistencia.html', views.asistencia, name='asistencia'),
  
]
