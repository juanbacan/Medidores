from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser, Medidor
# Register your models here.

admin.site.register(CustomUser)


class MedidorAdmin(admin.ModelAdmin):
    list_display = ('numero_medidor', 'cliente', 'direccion', 'tipo_consumo', 'meses_deuda', 'consumo', 'valor_mes', 'total_deuda')
    search_fields = ('numero_medidor', 'cliente__first_name', 'cliente__last_name', 'cliente__cedula')
    list_filter = ('tipo_consumo', 'meses_deuda')
    ordering = ('numero_medidor', 'cliente')
    list_per_page = 10

admin.site.register(Medidor, MedidorAdmin)

admin.site.site_header = 'Administración de Medidores'

admin.site.site_title = 'Administración de Medidores'

admin.site.index_title = 'Administración de Medidores'

admin.site.unregister(Group)
