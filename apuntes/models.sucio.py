from django.db import models

# Create your models here.

class Home(models.Model):
    nombre=models.CharField(max_length=50)
    greetings1=models.CharField(max_length=50)
    greetings2=models.CharField(max_length=50)
    picture=models.ImageField(upload_to= 'picture/')
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=200)
    correo_electronico = models.CharField(max_length=255)
    contrasena=models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Empleado(models.Model):
    #usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    nombre=models.CharField(max_length=100)
    apellido = models.CharField(max_length=200)
    dni=models.CharField(max_length=30)
    telefono=models.IntegerField
    lugar_trabajo=models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Asistencias(models.Model):
    empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE)
    fecha=models.DateField()
    entrada_hora=models.TimeField()
    entrada_ubicacion=models.CharField(max_length=200)
    salida_hora=models.TimeField()
    salida_ubicacion=models.CharField(max_length=200)
    area=models.CharField(max_length=100,blank=True, null=True)
    #para que se guarde automaticamente cada vez que se crea una instancia de usuario nueva
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.updated
    

class Incidencias(models.Model):
    empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE)
    fecha=models.DateField()
    hora= models.TimeField(auto_now_add=True)
    titulo=models.CharField(max_length=200)
    descripcion=models.CharField(max_length=10000)
    lugar=models.CharField(max_length=100)
    imagen=models.ImageField(upload_to= 'imagenes/')
    documentos=models.FileField(upload_to='documentos/')


    def __str__(self):
        return self.titulo
    
class Entrada(models.Model):
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)

    #empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE)
    fecha=models.DateField()
    hora_entrada=models.TimeField(auto_now_add=True)
    localizacion_entrada=models.CharField(max_length=500)
    def __str__(self):
        return self.empleado
    
class Salida(models.Model):
    empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE)
    fecha=models.DateField()
    hora_salida=models.TimeField(auto_now_add=True)
    localizacion_salida=models.CharField(max_length=500)
    def __str__(self):
        return self.empleado

    
