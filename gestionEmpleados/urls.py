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
    #path('login/guardar_salida/',views.guardar_salida,name='guardar_salida'),
    path('guardar_ficha/',views.guardar_ficha,name='guardar_ficha'),
    path('index.html/',views.index,name='index'),
    path('registros.html',views.registros,name='registros'),
    path('vista_entrada/',views.vista_entrada,name='vista_entrada'),
    path('vista_salida/',views.vista_salida,name='vista_salida'),
    path('vista_usuarios/',views.vista_usuario,name='vista_usuario'),
    path('registros_por_usuario/',views.registros_por_usuario,name='registros_por_usuario'),
    #path('entradas_nombre/',views.entradas_nombre,name='entradas_nombre'),
    path('entradas_nombre_usuario/<str:nombre_usuario>/',views.entradas_nombre,name='entradas_nombre'),
    path('salidas_por_usuario/<str:nombre_usuario>/',views.salidas_nombre,name='salidas_nombre')



  
]
