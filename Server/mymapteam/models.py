"""
Copyright (C) 2024 UTAI SOFTWARE

Este programa es software libre: puedes redistribuirlo y/o modificarlo bajo los términos de la Licencia Pública General de GNU publicada por la Free Software Foundation, ya sea la versión 3 de la Licencia, o (a tu elección) cualquier versión posterior.

Este programa se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulta los detalles de la Licencia Pública General de GNU para obtener más información.

Deberías haber recibido una copia de la Licencia Pública General de GNU junto con este programa. Si no es así, visita <https://www.gnu.org/licenses/>.

---

Copyright (C) 2024 UTAI SOFTWARE

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import uuid
import random
import string

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username


def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)  
    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveIntegerField()
    password = models.CharField(max_length=10, default=generate_random_password) 
    idmeet = models.CharField(max_length=32, unique=True, default=uuid.uuid4().hex)
    def __str__(self):
        return f'Reservation for {self.user.username} on {self.date} at {self.time} for {self.duration} hour(s)'


class Location(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    lat = models.FloatField()
    lng = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    pregunta = models.TextField()
    respuestaCorrecta = models.TextField()
    respuestaErronea = models.TextField()
    puntuacionRespuestaCorrecta = models.IntegerField(default=0)
    puntuacionRespuestaIncorrecta = models.IntegerField(default=0)
    def __str__(self):
        return self.pregunta


class PointOfInterest(models.Model):
    EVENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('pregunta', 'Pregunta')
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    color = models.CharField(max_length=7, default='#FF0000') 
    radius = models.FloatField(default=100) 
    created_at = models.DateTimeField(auto_now_add=True)
    valor = models.IntegerField(default=0)
    orden = models.PositiveIntegerField(null=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    enlace = models.CharField(max_length=500, blank=True, null=True) 
    tipoEvento = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, default='video')
    idPregunta = models.ForeignKey(Question, null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        unique_together = ('reservation', 'orden')
    def __str__(self):
        return self.name


class Objetivo(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)  
    concepto = models.TextField()  
    valor = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.concepto} - {self.profile.user.username} ({self.valor})"