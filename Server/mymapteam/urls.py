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

from django.urls import path
from . import views
from . import viewsApi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('',views.home, name='home'),
    path('home',views.privatehome, name='privatehome'),
    path('viewer/<str:idmeet>/', views.viewer, name='viewer'),
    path('viewer3/<str:idmeet>/', views.viewer3, name='viewer3'),
    path('update_location/', views.update_location, name='update_location'),
    path('disconnect/', views.disconnect, name='disconnect'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('make_reservation/', views.make_reservation, name='make_reservation'),
    path('reservation_summary/<str:idmeet>/', views.reservation_summary, name='reservation_summary'),
    path('add_point_of_interest/', views.add_point_of_interest, name='add_point_of_interest'),
    path('points_of_interest/<str:idmeet>/', views.list_points_of_interest, name='list_points_of_interest'),
    path('create_objective/', views.create_objective, name='create_objective'),
    path('obtener_puntos_usuario/<str:idmeet>/', views.obtener_puntos_usuario, name='obtener_puntos_usuario'),
    path('edit_point_of_interest/<int:point_id>/', views.edit_point_of_interest, name='edit_point_of_interest'),
    path('delete_point_of_interest/<int:point_id>/', views.delete_point_of_interest, name='delete_point_of_interest'),
    path('get_user_location/<int:user_id>/', views.get_user_location, name='get_user_location'),
    path('get_question/<int:question_id>/', views.get_question, name='get_question'),
    path('api/update_locationApi/', views.update_locationApi, name='update_locationApi'),
    path('api/get_locations/', viewsApi.get_locations, name='get_locations'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify-token/', views.verify_token, name='verify_token'),  
    path('api/get_locationsApi/', viewsApi.get_locationsApi, name='get_locationsApi'),

]
