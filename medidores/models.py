from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    cedula = models.CharField(max_length=10, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    celular = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name + ' - ' + self.cedula
        return self.username
    
    class Meta:
        unique_together = ('cedula', 'email')
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Medidor(models.Model):

    CHOICE_TIPO_CONSUMO = (
        ('Residencial', 'Residencial'),
        ('Comercial', 'Comercial'),
        ('Industrial', 'Industrial'),
    )

    # cedula = models.CharField(max_length=10)
    numero_medidor = models.CharField(max_length=10, unique=True)
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100)
    tipo_consumo = models.CharField(max_length=20, choices=CHOICE_TIPO_CONSUMO)
    meses_deuda = models.IntegerField(default=0)
    consumo = models.FloatField(default=0)
    valor_mes = models.FloatField(default=0)
    total_deuda = models.FloatField(default=0)

    def __str__(self):
        return self.numero_medidor
    
    class Meta:
        unique_together = ('numero_medidor', 'cliente')
        verbose_name = 'Medidor'
        verbose_name_plural = 'Medidores'