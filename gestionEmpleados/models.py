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
    id_usuario=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=200)
    #posicion=models.Charfield(max_length=30)
    correo_electronico = models.CharField(max_length=255)
    contrasena=models.CharField(max_length=100)
    
    def __str__(self):
        return self.apellido
    
class Empleado(Usuario):
    id_empleado=models.AutoField(primary_key=True, default=0)
    id_usuario=Usuario.id_usuario
    nombre=Usuario.nombre
    apellido=Usuario.apellido
    dni=models.CharField(max_length=30)
    telefono=models.IntegerField
    lugar_trabajo=models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class Gestores(Usuario):
    id_gestor=models.AutoField(primary_key=True, default=0)
    id_usuario=Usuario.id_usuario
    nombre=Usuario.nombre
    apellido=Usuario.apellido
    cargo=models.CharField(max_length=200)
    oficina=models.CharField(max_length=100)

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
    
"""class Entrada(models.Model):
    id_entrada=models.AutoField(primary_key=True)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name='entradas')
    nombre_usuario=models.CharField(max_length=200)
    fecha=models.DateField()
    hora_entrada=models.TimeField(auto_now_add=True)
    localizacion_entrada=models.CharField(max_length=500)
      class Meta:
        db_table='entrada'
        managed=True
        #para que se muestren primero las horas de entrada mas tempranas dentro de una misma fecha
        ordering=['fecha','hora_entrada']

    def __str__(self):
        return self.nombre_usuario"""

class Entrada(models.Model):
    id_entrada=models.AutoField(primary_key=True)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name='entradas')
    nombre_usuario=models.CharField(max_length=200)
    fecha=models.DateField()
    hora=models.TimeField(auto_now_add=True)
    coordenadas=models.CharField(max_length=500)
    direccion=models.CharField(max_length=1000)
    link_mapa=models.CharField(max_length=1000)

    def __str__(self):
        return self.nombre_usuario

    

    """
    @property
    def nombre_usuario(self):
        return self.usuario.nombre
    """
    
    
  
    
class Salida(models.Model):
    id_salida=models.AutoField(primary_key=True)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name='salidas')
    nombre_usuario=models.CharField(max_length=200)
    fecha=models.DateField()
    hora=models.TimeField(auto_now_add=True)
    coordenadas=models.CharField(max_length=500)
    direccion=models.CharField(max_length=1000)
    link_mapa=models.CharField(max_length=1000)

    def __str__(self):
        return self.nombre_usuario

    
