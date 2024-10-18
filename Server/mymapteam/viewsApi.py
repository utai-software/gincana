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
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from .forms import ReservationForm, CustomUserCreationForm, PointOfInterestForm
from .models import Reservation, PointOfInterest, Location, Objetivo, Profile



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_locations(request):
    idmeet = request.query_params.get('idmeet')
    try:
        reservation = Reservation.objects.get(idmeet=idmeet)
    except Reservation.DoesNotExist:
        return Response({'error': 'Reservation not found'}, status=404)
    locations = Location.objects.filter(reservation=reservation).order_by('-timestamp')
    data = [
        {
            'name': loc.name,
            'lat': loc.lat,
            'lng': loc.lng,
            'timestamp': loc.timestamp
        }
        for loc in locations
    ]
    return Response({'locations': data})


def update_locationApi(request):
    body = json.loads(request.body)
    token = body.get('token')
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
    except:
        return JsonResponse({'error': 'Token inválido o expirado'}, status=401)
    lat = body.get('lat')
    lng = body.get('lng')
    idmeet = body.get('idmeet')

    if not lat or not lng or not idmeet:
        return JsonResponse({'error': 'Faltan parámetros obligatorios'}, status=400)
    user = User.objects.get(id=user_id)
    try:
        reservation = Reservation.objects.get(idmeet=idmeet, user=user)
    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'Sesión no encontrada o usuario no autorizado'}, status=404)
    Location.objects.create(
        reservation=reservation,
        name=user.username,
        lat=lat,
        lng=lng
    )

    return JsonResponse({'success': 'Ubicación actualizada correctamente'}, status=200)

def get_locationsApi(request):
    if request.method == 'GET':
        idmeet = request.query_params.get('idmeet')  

        if not idmeet:
            return Response({'error': 'idmeet parameter is required'}, status=400)
        
        try:
            reservation = Reservation.objects.get(idmeet=idmeet)
        except Reservation.DoesNotExist:
            return Response({'error': 'Reservation not found'}, status=404)
        locations = Location.objects.filter(reservation=reservation).order_by('-timestamp')
        data = [
            {
                'name': loc.name,
                'lat': loc.lat,
                'lng': loc.lng,
                'color': loc.color,  
                'timestamp': loc.timestamp
            }
            for loc in locations
        ]
        # Devolvemos las ubicaciones en formato JSON
        return Response({'locations': data}, status=200)