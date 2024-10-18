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


import json
import random
import string
import uuid
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm, ReservationForm, PointOfInterestForm
from .models import Reservation, Location, Objetivo, Profile, PointOfInterest, Question


def user_login(request):
    if request.method == 'POST':
        print("USER LOGIN")
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('privatehome')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def privatehome(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'privatehome.html', {'reservations': reservations})


@login_required
def viewer3(request, idmeet):
    reservation = get_object_or_404(Reservation, idmeet=idmeet)
    locations = reservation.locations.all()
    reservation = get_object_or_404(Reservation, idmeet=idmeet)
    profile = request.user.profile
    user = request.user
    total_puntos = Objetivo.objects.filter(profile=profile, reservation=reservation).aggregate(Sum('valor'))['valor__sum'] or 0
    points = PointOfInterest.objects.filter(reservation=reservation)
    points_data = json.dumps(list(points.values('name', 'description', 'lat', 'lng', 'radius','enlace','tipoEvento','idPregunta_id','valor')))
    is_creator = request.user == reservation.user
    return render(request, 'viewer.html', {
        'reservation': reservation,
        'locations': locations,
        'logged_in_user': user.username, 
        'points': points_data,
        'logged_In_user_ID': user.id,
        'total_puntos': total_puntos, 
        'is_creator': is_creator,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    })    


@login_required
def viewer(request, idmeet):
    reservation = get_object_or_404(Reservation, idmeet=idmeet)
    if request.method == 'GET':
        return render(request, 'password_form.html', {'idmeet': idmeet})
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == reservation.password:
            locations = reservation.locations.all()
            reservation = get_object_or_404(Reservation, idmeet=idmeet)
            profile = request.user.profile
            user = request.user  
            total_puntos = Objetivo.objects.filter(profile=profile, reservation=reservation).aggregate(Sum('valor'))['valor__sum'] or 0
            points = PointOfInterest.objects.filter(reservation=reservation)
            points_data = json.dumps(list(points.values('name', 'description', 'lat', 'lng', 'radius','enlace','tipoEvento','idPregunta_id','valor')))
            is_creator = request.user == reservation.user
            return render(request, 'viewer.html', {
                'reservation': reservation,
                'locations': locations,
                'logged_in_user': user.username, 
                'points': points_data,
                'logged_In_user_ID': user.id,
                 'total_puntos': total_puntos,  
                'is_creator': is_creator,
                'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
            })
        else:
            return HttpResponse('Contraseña incorrecta', status=401)


@csrf_exempt
def update_location(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            idmeet = data.get('idmeet')
            reservation = get_object_or_404(Reservation, idmeet=idmeet)
            Location.objects.create(
                reservation=reservation,
                name=data['name'],
                color=data['color'],
                lat=data['lat'],
                lng=data['lng'],
            )
            return JsonResponse({'status': 'success'})
        elif request.method == 'GET':
            idmeet = request.GET.get('idmeet')
            reservation = get_object_or_404(Reservation, idmeet=idmeet)
            locations = reservation.locations.all()
            locations_data = [{'name': loc.name, 'color': loc.color, 'lat': loc.lat, 'lng': loc.lng, 'timestamp': loc.timestamp} for loc in locations]
            return JsonResponse({'locations': locations_data})
    except Exception as e:
        print(f"Error: {e}")  
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def disconnect(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        return JsonResponse({'status': 'disconnected'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.user_name = request.user.get_full_name() or request.user.username
            reservation.idmeet = form.cleaned_data.get('idmeet', uuid.uuid4().hex)  
            reservation.password = form.cleaned_data.get('password', generate_random_password())  
            reservation.save()
            messages.success(request, 'Reserva realizada con éxito')
            return redirect('reservation_summary', idmeet=reservation.idmeet)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {form.fields[field].label}: {error}")
    else:
        random_password = generate_random_password()
        form = ReservationForm(initial={'idmeet': uuid.uuid4().hex ,'password': random_password})
    return render(request, 'make_reservation.html', {'form': form})


@login_required
def reservation_summary(request, idmeet):
    reservation = get_object_or_404(Reservation, idmeet=idmeet)
    return render(request, 'reservation_summary.html', {'reservation': reservation})


def add_point_of_interest(request):
    idmeet = request.GET.get('idmeet')
    reservation = get_object_or_404(Reservation, idmeet=idmeet)

    if request.method == 'POST':
        form = PointOfInterestForm(request.POST)
        tipo_evento = request.POST.get('tipoEvento')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        raidus = request.POST.get('radius')
        descripcion = request.POST.get('descripcion')

        if form.is_valid() and lat and lng:
            point = form.save(commit=False)
            point.lat = lat
            point.lng = lng
            point.reservation = reservation
            point.tipoEvento = tipo_evento
            point.radius = request.POST.get('radius')
            point.description = descripcion

            if tipo_evento == 'pregunta':
                pregunta = request.POST.get('pregunta')
                respuesta_correcta = request.POST.get('respuestaCorrecta')
                respuesta_erronea = request.POST.get('respuestaErronea')
                puntuacion_correcta = request.POST.get('puntuacionCorrecta')
                puntuacion_incorrecta = request.POST.get('puntuacionIncorrecta')

                question = Question.objects.create(
                    pregunta=pregunta,
                    respuestaCorrecta=respuesta_correcta,
                    respuestaErronea=respuesta_erronea,
                    puntuacionRespuestaCorrecta=puntuacion_correcta,
                    puntuacionRespuestaIncorrecta=puntuacion_incorrecta
                )
                point.idPregunta = question
            if tipo_evento == 'video':
                point.valor = request.POST.get('valor')
                point.enlace = request.POST.get('enlace')
            point.save()
            return redirect('viewer3', idmeet=idmeet)
    else:
        form = PointOfInterestForm()

    return render(request, 'add_point_of_interest.html', {'form': form, 'idmeet': idmeet, 'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY})

 
def list_points_of_interest(request, idmeet):
    reservation = get_object_or_404(Reservation, idmeet=idmeet)
    points = PointOfInterest.objects.filter(reservation=reservation).select_related('idPregunta')
    points_data = []
    for point in points:
        point_data = {
            'id': point.id,
            'name': point.name,
            'description': point.description,
            'lat': point.lat,
            'lng': point.lng,
            'radius': point.radius,
            'tipoEvento': point.tipoEvento,
            'valor': point.valor,
            'enlace': point.enlace,
            'idPregunta_id': point.idPregunta_id,
        }

        if point.tipoEvento == 'pregunta' and point.idPregunta:
            question = point.idPregunta
            point_data.update({
                'pregunta': question.pregunta,
                'respuestaCorrecta': question.respuestaCorrecta,
                'respuestaErronea': question.respuestaErronea,
                'puntuacionCorrecta': question.puntuacionRespuestaCorrecta,
                'puntuacionIncorrecta': question.puntuacionRespuestaIncorrecta,
            })
        points_data.append(point_data)
    points_json = json.dumps(points_data)

    return render(request, 'list_points_of_interest.html', {'points': points_json, 'reservation': reservation, 'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY})


def create_objective(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        user_name = data.get('user_name')
        idmeet = data.get('idmeet')
        concepto = data.get('concepto')
        valor = data.get('valor')
        print(f" User: {user_name}, IDMeet: {idmeet}, Concept: {concepto}, Value: {valor}")
        try:
            profile = Profile.objects.get(user__username=user_name)
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        try:
            reservation = Reservation.objects.get(idmeet=idmeet)
        except Reservation.DoesNotExist:
            return JsonResponse({'error': 'Reserva no encontrada'}, status=404)

        print(f"{concepto}")
        if Objetivo.objects.filter(profile=profile, reservation=reservation, concepto=concepto).exists():
            return JsonResponse({'message': 'El objetivo ya existe. No se creará un nuevo registro.'}, status=200)

        valor = Decimal(valor)
        print(f"{valor} (Type: {type(valor)})")
        nuevo_objetivo = Objetivo.objects.create(
            profile=profile,
            reservation=reservation,
            concepto=concepto,
            valor=valor
        )
        print(f"Objetivo creado correctamente con valor: {nuevo_objetivo.valor}")
        return JsonResponse({'message': 'Objetivo creado correctamente'}, status=201)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def obtener_puntos_usuario(request, idmeet):
    if request.user.is_authenticated:
        try:
            reservation = Reservation.objects.get(idmeet=idmeet)
            total_puntos = Objetivo.objects.filter(profile=request.user.profile, reservation=reservation).aggregate(Sum('valor'))['valor__sum'] or 0
            return JsonResponse({'total_puntos': total_puntos})
        except Reservation.DoesNotExist:
            return JsonResponse({'error': 'Reserva no encontrada'}, status=404)
    return JsonResponse({'error': 'Usuario no autenticado'}, status=401)


@csrf_exempt
def edit_point_of_interest(request, point_id):
    if request.method == 'POST':
        try:
            point = PointOfInterest.objects.get(id=point_id)
            data = json.loads(request.body)
            print(f"DATA  ::::   {data}")
            if 'name' in data:
                point.name = data['name']

            if 'description' in data:
                point.description = data['description']
            
            if 'lat' in data and 'lng' in data:
                point.lat = data['lat']
                point.lng = data['lng']

            if 'tipoEvento' in data:
                point.tipoEvento = data['tipoEvento']
                point.enlace = ''
                point.valor = 0
                point.idPregunta = None

                if point.tipoEvento == 'video':
                    point.enlace = data.get('enlace', '')
                    point.valor = int(data.get('valor', 0))

                elif point.tipoEvento == 'pregunta':
                    new_question = Question(
                        pregunta=data.get('pregunta', ''),
                        respuestaCorrecta=data.get('respuestaCorrecta', ''),
                        respuestaErronea=data.get('respuestaErronea', ''),
                        puntuacionRespuestaCorrecta=int(data.get('puntuacionCorrecta', 0)),
                        puntuacionRespuestaIncorrecta=int(data.get('puntuacionIncorrecta', 0))
                    )
                    new_question.save()  
                    point.idPregunta = new_question

            point.save()
            return JsonResponse({'success': True})
        except PointOfInterest.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Punto de interés no encontrado'}, status=404)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


@csrf_exempt
def delete_point_of_interest(request, point_id):
    if request.method == 'POST':
        try:
            point = get_object_or_404(PointOfInterest, id=point_id)
            point.delete()

            return JsonResponse({'success': True})
        except PointOfInterest.DoesNotExist:
            return JsonResponse({'error': 'Punto de interés no encontrado.'}, status=404)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)


def update_locationApi(request):
    verify_response = verify_token(request)
    if verify_response.status_code == 200:
        verify_data = json.loads(verify_response.content)
        user_id = verify_data.get('user_id')
    else:
        return verify_response  
    print(user_id)
    body = json.loads(request.body)
    lat = body.get('lat')
    lng = body.get('lng')
    idmeet = body.get('idmeet')
    user = User.objects.get(id=user_id)
    print(lat)
    print(lng)
    print(idmeet)
    print(user.username)
    print(user_id)
    try:
        reservation = Reservation.objects.get(idmeet=idmeet, user=2)
    except Reservation.DoesNotExist:
        return Response({'error': 'Reservation not found'}, status=404)
    print(reservation.user.username)
    location = Location.objects.create(
        reservation=reservation,
        name=user.username,
        lat=lat,
        lng=lng,
    )
    print(location)

    return JsonResponse({'success': 'Location updated'})


def verify_token(request):
    try:
        body = json.loads(request.body)
        token = body.get('token')  
        access_token = AccessToken(token)   
        user_id = access_token['user_id']  
        return JsonResponse({'access_token': str(access_token), 'user_id': user_id})
    except KeyError:
        return JsonResponse({'valid': False, 'error': 'Token not provided'}, status=400)
    except Exception as e:
        return JsonResponse({'valid': False, 'error': str(e)}, status=401)


def get_user_location(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        username = user.username
        print(f"{username}")
        location = Location.objects.filter(name =username).latest('timestamp')
        print(f"{location}")
        return JsonResponse({
            'lat': location.lat,
            'lng': location.lng,
            'name': location.name,
            'timestamp': location.timestamp
        })
    except Location.DoesNotExist:
        return JsonResponse({'error': 'Location not found'}, status=404)
    

def get_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return JsonResponse({
        'pregunta': question.pregunta,
        'respuestaCorrecta': question.respuestaCorrecta,
        'respuestaErronea': question.respuestaErronea,
        'puntuacionCorrecta': question.puntuacionRespuestaCorrecta,
        'puntuacionIncorrecta': question.puntuacionRespuestaIncorrecta
    })