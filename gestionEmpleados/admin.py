from django.contrib import admin
from .models import Usuario, Empleado,Asistencias,Incidencias,Home,Entrada,Gestores,Salida

admin.site.register(Home)
admin.site.register(Usuario)
admin.site.register(Empleado)
admin.site.register(Asistencias)
admin.site.register(Incidencias)
admin.site.register(Entrada)
admin.site.register(Gestores)
admin.site.register(Salida)

"""
class EmpleadoInline(admin.TabularInline):
    model=Empleado
    extra=7
@admin.register(Asistencias)
class AsistenciasAdmin(admin.ModelAdmin):
    inlines=[
        EmpleadoInline,
    ]
"""





