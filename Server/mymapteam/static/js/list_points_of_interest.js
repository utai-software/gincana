/*
Copyright (C) 2024 UTAI SOFTWARE

Este programa es software libre: puedes redistribuirlo y/o modificarlo bajo los términos de la Licencia Pública General de GNU publicada por la Free Software Foundation, ya sea la versión 3 de la Licencia, o (a tu elección) cualquier versión posterior.

Este programa se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulta los detalles de la Licencia Pública General de GNU para obtener más información.

Deberías haber recibido una copia de la Licencia Pública General de GNU junto con este programa. Si no es así, visita <https://www.gnu.org/licenses/>.

---

Copyright (C) 2024 UTAI SOFTWARE

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

let map;
let markers = {};
initMap();

async function initMap() {
    const centerLocation = { lat: 40.416775, lng: -3.703790 };  // Madrid como ubicación central
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 6,
        center: centerLocation
    });

    const mapDataElement = document.getElementById('map-data');
    const points = JSON.parse(mapDataElement.dataset.points); 
    console.log(points);

    points.forEach(function (point) {
        const marker = new google.maps.Marker({
            position: { lat: parseFloat(point.lat), lng: parseFloat(point.lng) },
            map: map,
            title: point.name,
            draggable: true
        });

        markers[point.id] = marker;

        const infoWindowContent = `
            <div>
                <h5>Editar Punto: ${point.name}</h5>
                <div class="form-group">
                    <label for="name_${point.id}">Nombre:</label>
                    <input type="text" id="name_${point.id}" class="form-control" value="${point.name}">
                </div>
                <div class="form-group">
                    <label for="description_${point.id}">Descripción:</label>
                    <textarea id="description_${point.id}" class="form-control" rows="3">${point.description || ''}</textarea>
                </div>
                <div class="form-group">
                    <label for="tipoEvento_${point.id}">Tipo de Evento:</label>
                    <select id="tipoEvento_${point.id}" class="form-control" onchange="toggleFields(${point.id})">
                        <option value="">Seleccionar...</option>
                        <option value="video" ${point.tipoEvento === 'video' ? 'selected' : ''}>Video</option>
                        <option value="pregunta" ${point.tipoEvento === 'pregunta' ? 'selected' : ''}>Pregunta</option>
                    </select>
                </div>
                <div id="videoFields_${point.id}" style="display: ${point.tipoEvento === 'video' ? 'block' : 'none'};">
                    <div class="form-group">
                        <label for="enlace_${point.id}">ID del Video:</label>
                        <input type="text" id="enlace_${point.id}" class="form-control" value="${point.enlace || ''}">
                    </div>
                    <div class="form-group">
                        <label for="valor_${point.id}">Valor:</label>
                        <input type="number" id="valor_${point.id}" class="form-control" value="${point.valor || 0}">
                    </div>
                </div>
                <div id="preguntaFields_${point.id}" style="display: ${point.tipoEvento === 'pregunta' ? 'block' : 'none'};">
                    <div class="form-group">
                        <label for="pregunta_${point.id}">Pregunta:</label>
                        <input type="text" id="pregunta_${point.id}" class="form-control" value="${point.pregunta || ''}">
                    </div>
                    <div class="form-group">
                        <label for="respuestaCorrecta_${point.id}">Respuesta Correcta:</label>
                        <input type="text" id="respuestaCorrecta_${point.id}" class="form-control" value="${point.respuestaCorrecta || ''}">
                    </div>
                    <div class="form-group">
                        <label for="respuestaErronea_${point.id}">Respuesta Incorrecta:</label>
                        <input type="text" id="respuestaErronea_${point.id}" class="form-control" value="${point.respuestaErronea || ''}">
                    </div>
                    <div class="form-group">
                        <label for="puntuacionCorrecta_${point.id}">Puntuación Correcta:</label>
                        <input type="number" id="puntuacionCorrecta_${point.id}" class="form-control" value="${point.puntuacionCorrecta || 0}">
                    </div>
                    <div class="form-group">
                        <label for="puntuacionIncorrecta_${point.id}">Puntuación Incorrecta:</label>
                        <input type="number" id="puntuacionIncorrecta_${point.id}" class="form-control" value="${point.puntuacionIncorrecta || 0}">
                    </div>
                </div>
                <button class="btn btn-success btn-sm" onclick="saveChanges(${point.id})">Guardar Cambios</button>
                <button class="btn btn-danger btn-sm" onclick="deletePoint(${point.id})">Eliminar</button>
            </div>
        `;

        const infoWindow = new google.maps.InfoWindow({
            content: infoWindowContent
        });

        marker.addListener('click', function () {
            infoWindow.open(map, marker);
        });
    });
}

function toggleFields(pointId) {
    const tipoEvento = document.getElementById(`tipoEvento_${pointId}`).value;
    document.getElementById(`videoFields_${pointId}`).style.display = tipoEvento === 'video' ? 'block' : 'none';
    document.getElementById(`preguntaFields_${pointId}`).style.display = tipoEvento === 'pregunta' ? 'block' : 'none';
}

function saveChanges(pointId) {
    const tipoEvento = document.getElementById(`tipoEvento_${pointId}`).value;

    let data = {
        name: document.getElementById(`name_${pointId}`).value,
        description: document.getElementById(`description_${pointId}`).value,
        tipoEvento: tipoEvento,
        lat: markers[pointId].getPosition().lat(),
        lng: markers[pointId].getPosition().lng()
    };

    if (tipoEvento === 'video') {
        data.enlace = document.getElementById(`enlace_${pointId}`)?.value || '';
        data.valor = parseInt(document.getElementById(`valor_${pointId}`)?.value || 0);
    } else if (tipoEvento === 'pregunta') {
        data.pregunta = document.getElementById(`pregunta_${pointId}`)?.value || '';
        data.respuestaCorrecta = document.getElementById(`respuestaCorrecta_${pointId}`)?.value || '';
        data.respuestaErronea = document.getElementById(`respuestaErronea_${pointId}`)?.value || '';
        data.puntuacionCorrecta = parseInt(document.getElementById(`puntuacionCorrecta_${pointId}`)?.value || 0);
        data.puntuacionIncorrecta = parseInt(document.getElementById(`puntuacionIncorrecta_${pointId}`)?.value || 0);
    }

    fetch(`/edit_point_of_interest/${pointId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Cambios guardados correctamente.');
                location.reload();
            } else {
                alert('Error al guardar los cambios.');
            }
        });
}

function deletePoint(pointId) {
    if (confirm("¿Estás seguro de que quieres eliminar este punto de interés?")) {
        fetch(`/delete_point_of_interest/${pointId}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') }
        }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Punto de interés eliminado.');
                    location.reload();
                } else {
                    alert('Error al eliminar el punto de interés.');
                }
            });
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
