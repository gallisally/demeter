from django.shortcuts import render
from .models import Home,Usuario,Entrada,Empleado
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

        # Validar las credenciales
        if usuario is not None and usuario.contrasena == contrasena:
            # Iniciar sesión al usuario
            request.session["usuario_id"] = usuario.id_usuario

            return redirect("asistencia.html")

    return render(request, "asistencia.html")



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
            coordenadas_usuario=(latitud,longitud)
            print('tu localizacion se ha cogido satisfactoriamente')
            print(f"Latitud: {latitud}, Longitud: {longitud}")
            print(f"Dirección: {direccion}") 

            # Obtén o crea un objeto Empleado relacionado con el usuario actual
            #usuario, creado = Empleado.objects.get_or_create(usuario=request.user)
            usuario=request.user
            #usuario=Usuario.object.get_or_create(usuario=request.user)
            entrada=Entrada(
                id_usuario=usuario.id_usuario,
                nombre=usuario.nombre,

                #usuario=usuario,
                #empleado=request.user,
                fecha=timezone.now().date,
                hora_entrada=timezone.now().time(),
                localizacion_entrada=direccion

            )
            entrada.save()  
            
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
        print(f'la precision es {precision}')
        print(f'la localizacion es : {localizacion}')
        entrada=Entrada(
            empleado=request.user,
            fecha=timezone.now().date,
            hora_entrada=timezone.now().time(),
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







