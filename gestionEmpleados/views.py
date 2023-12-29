from django.shortcuts import render
from .models import Home,Usuario,Entrada,Empleado,Salida
from django.shortcuts import redirect
import geolocation

from django.utils import timezone
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import geopy
from geopy.geocoders import Nominatim

import certifi
import ssl
from geopy.distance import geodesic

import geopy.geocoders
from geopy.geocoders import Nominatim
#from geopy.geocoder import geocoder
import geocoder
from django.contrib.auth.decorators import login_required 
from datetime import datetime
import time
from django.http import HttpResponse
from .models import Usuario
from django.shortcuts import get_object_or_404
import requests
import geolocation
from django.http import JsonResponse
import json


# Create your views here.
def index(request):
    home=Home.objects.latest('updated')
    #enviando variable a template
    context={
        'home': home,
    }
    #inviando context alla richiesta
    return render(request,'index.html',context)

def crear_usuario(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido= request.POST.get('apellido')
        correo_electronico = request.POST.get("correo_electronico")
        contrasena = request.POST.get("contrasena")

        # Guardar el usuario en la base de datos
        usuario = Usuario(nombre=nombre,apellido=apellido, correo_electronico=correo_electronico, contrasena=contrasena)
        usuario.save()
        

        return redirect("/")

    return render(request, "crear_usuario.html")

def login(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        contrasena = request.POST.get("contrasena")

        # Obtener el usuario de la base de datos
        usuario = Usuario.objects.filter(nombre=nombre).first()
        #print(f'el usuario es {usuario.nombre}')
        # Validar las credenciales
        if usuario is not None and usuario.contrasena == contrasena:
            # Iniciar sesión al usuario y guardar nombre e id de la sesion iniciada
            request.session["id_usuario"] = usuario.id_usuario
            request.session["nombre"] = usuario.nombre
            return redirect("asistencia.html")

    #return render(request, "asistencia.html")



def localizar_coordenadas(direccion):
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx

    geolocalizador=Nominatim(user_agent='draco')
    #direccion='73 Calle Ramon y Cajal, Torrevieja, Spain'
    localizador=geolocalizador.geocode(direccion)
    direccion_completa=localizador.address
    latitud_direccion=localizador.latitude
    longitud_direccion=localizador.longitude
    coordenadas_lugar=(latitud_direccion,longitud_direccion)

    if localizador:
        print(f'Direccion: {direccion_completa}')
        print(f'Coordenadas: {latitud_direccion}(lattitud),{longitud_direccion}(longitud)')

    else:
        print('no se ha encontrado la localizacion')

    return coordenadas_lugar

#def posicion_usuario():
@login_required
def geolocalizacion(request):
    if request.method=='POST':
        ubicacion_usuario=geocoder.ip('me')
        if ubicacion_usuario.ok:
            latitud = ubicacion_usuario.latlng[0]
            longitud = ubicacion_usuario.latlng[1]
            direccion = ubicacion_usuario.address
            #coordenadas_usuario=(latitud,longitud)
            print('tu localizacion se ha cogido satisfactoriamente')
            print(f"Latitud: {latitud}, Longitud: {longitud}")
            print(f"Dirección: {direccion}") 
            print(f' la ip es : {ubicacion_usuario}')

            id_usuario=request.session.get("id_usuario")
            nombre_usuario=request.session.get("nombre")
            print(f'nombre de usuario en geol{nombre_usuario}')
            print(f'el id  en geol es {id_usuario}')
            # Retrieve the Usuario instance from the database
            usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
            print(f'el usuario es: {usuario}')

            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitud}&lon={longitud}"
            response=requests.get(url)
            data=response.json()
            address=data['display_name']
            print(f'la direccion comlpeta es: {address}')
            location = geopy.geocoders.Nominatim(user_agent="gestionEmpleados")
            print(f'la direccion comlpeta es de location: {location}')
 
            fecha=datetime.now().date()
            hora_entrada=datetime.now().time()



            entrada=Entrada(
                usuario=usuario,
                nombre_usuario=nombre_usuario,
                #usuario=usuario,
                #empleado=request.user,
                fecha=fecha,
                hora_entrada=hora_entrada,
                localizacion_entrada=direccion

            )
            entrada.save()  
        return HttpResponse('la entrada se ha guardado correctamente')

@csrf_exempt  # Añade este decorador si la vista recibe datos mediante POST
def guardar_ficha(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tipo=data.get("tipo")
        
        # Accede a los datos específicos que necesitas
        direccion = data.get("direccion")
        coordenadas = data.get("coordenadas")
        link_mapa = data.get("link_mapa")
        
        #coordenadas = request.POST.get("coordenadas")
        id_usuario=request.session.get("id_usuario")
        nombre_usuario=request.session.get("nombre")
        fecha=datetime.now().date()
        hora=datetime.now().time()
        print(f'el id del usuario es: {id_usuario}')
        print(f'el link del mapa es {link_mapa}')
        print(f'el nombre del usuario es {nombre_usuario}')
        print(f' las coordenadas de la posicion son {coordenadas}')
        print(f'la fecha de la salida es : {fecha}')
        print(f'la hora : {hora}')
        print(f' la direcion es {direccion}')
        usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        if tipo == 'entrada':
            fichaje= Entrada(usuario=usuario,nombre_usuario=nombre_usuario,fecha=fecha,hora=hora,coordenadas=coordenadas,direccion=direccion,link_mapa=link_mapa)
            fichaje.save()
        if tipo=='salida':
            fichaje=Salida(usuario=usuario,nombre_usuario=nombre_usuario,fecha=fecha,hora=hora,coordenadas=coordenadas,direccion=direccion,link_mapa=link_mapa)
            fichaje.save()
        #return redirect("/")
        return JsonResponse({'message': 'Datos Guardados con exito'})
        #print('fatos guardados correctamente')
        #return render(request, "asistencia.html", {})

    
    else:
        return JsonResponse({'message': ' Método de solicitud POST no valido'})





         
def asistencia(request):
    return render(request, 'asistencia.html')

def checkear_posicion(coordenadas_lugar,coordenadas_usuario):

    
    # Radio en metros para considerar "dentro" de la ubicación deseada
    radio = 1000  # Puedes ajustar este valor según tus necesidades

    # Calcular la distancia entre las coordenadas del usuario y la ubicación deseada
    distancia = geodesic(coordenadas_lugar, coordenadas_usuario).meters

    # Verificar si el usuario está dentro del radio deseado
    if distancia <= radio:
        print("El usuario está dentro de la ubicación deseada.")
    else:
        print("El usuario está fuera de la ubicación deseada.")





def geolocalizacion_2(request):
    if request.method=='POST':
        ip_address = request.META.get('REMOTE_ADDR')
        localizador=Nominatim(user_agent='gestionEmpleados')
        localizacion = localizador.reverse(ip_address)
        latitud=localizacion.latitude
        longitud=localizacion.longitude
        coordenadas=localizador.reverse(latitud,longitud)
        ubicacion=coordenadas.address()
        precision=localizacion.accuracy()
        fecha=datetime.now().date()
        hora_entrada=datetime.now().time()
        print(f'la precision es {precision}')
        print(f'la localizacion es : {localizacion}')
        entrada=Entrada(
            empleado=request.user,
            fecha=timezone.now(),
            hora_entrada=timezone.now(),
            #hora_entrada=timezone.now().time(),
            localizacion_entrada=ip_address

        )
        
        
        entrada.save()
    return ubicacion

@csrf_protect
def geolocalizacion_1(request):
    if request.method == 'POST':
        location = geolocation.getCurrentPosition()
        entrada = Entrada(
            empleado=request.user,
            fecha=timezone.now().date(),
            hora_entrada=timezone.now().time(),
            localizacion_entrada=location
        )
        entrada.save()
        return entrada
    #return render(request, "asistencia.html")

def geoloc_prueba(request):
    if request.method=='POST':
        location=geolocation.get_location(lambda location: geolocation.save_location(location))
    return location

def geolocation_change(request):
    if request.method=='POST':
        geolocation.on_location_changed(lambda location_changed: geolocation.save_location(location_changed))
        geolocation.start()
        return geolocation.get_last_location


def consulta_ultima_ubicacion(request):
    if request.method =='POST':
        location=geolocation.get_last_location()
        if location:
            print(location)
        else:
            print('No se ha guardado ningun cambio en la ubicacion')

def registros(request):
    return render(request,'registros.html')

def vista_entrada(request):
    entradas=Entrada.objects.all()
    return render(request, 'entradas.html', {'entradas': entradas})

def vista_salida(request):
    salidas=Salida.objects.all()
    return render(request,'salidas.html',{'salidas': salidas})
def vista_usuario(request):
    usuarios=Usuario.objects.all()
    return render(request,'usuarios.html', {'usuarios': usuarios})

def registros_por_usuario(request):
    if request.method == "GET" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        nombre_usuario=request.GET.get('nombre_usuario')
        tipo=request.GET.get('tipo')
        print(f'el nombre de usuario es {nombre_usuario}')
        print(f'el tipo de tabla es :{tipo}')
        if tipo == 'entrada':
            #filtrar por nombre de la fila seleccionada
            entradas=Entrada.objects.filter(nombre_usuario=nombre_usuario) 
            datos=[{'nombre_usuario':entrada.nombre_usuario,'fecha':entrada.fecha,'hora':entrada.hora,'coordenadas':entrada.coordenadas,'direccion':entrada.direccion,'link_mapa':entrada.link_mapa,'usuario_id':entrada.usuario_id} for entrada in entradas]
            return JsonResponse({'entradas': datos})
        elif tipo =='salida':
            salidas=Salida.objects.filter(nombre_usuario=nombre_usuario)
            datos=[{'nombre_usuario':salida.nombre_usuario,'fecha':salida.fecha,'hora':salida.hora,'coordenadas':salida.coordenadas,'direccion':salida.direccion,'link_mapa':salida.link_mapa,'usuario_id':salida.usuario_id} for salida in salidas]      
            return JsonResponse({'salidas': datos})
    return JsonResponse({'error': 'No se ha podido acceder a los registros correspondientes del usuario'})

def entradas_nombre(request,nombre_usuario):
    entradas=Entrada.objects.filter(nombre_usuario=nombre_usuario)
    return render(request, 'entradas_nombre_usuario.html',{'entradas': entradas})

def salidas_nombre(request,nombre_usuario):
    salidas=Salida.objects.filter(nombre_usuario=nombre_usuario)
    return render(request,'salidas_por_usuario.html',{'salidas':salidas})





