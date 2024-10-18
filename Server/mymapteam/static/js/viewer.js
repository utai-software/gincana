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
const mapDataElement = document.getElementById('map-data');

const userDataElement = document.getElementById('user-data'); 
let map;
let markers = {};
let infoWindows = {};
let circles = {}; 
let locationsList;
let userName = userDataElement.dataset.loggedInUser;
let userColor = '';
let refreshInterval = 5000;  // Default refresh interval
let watchId;
const idmeet = userDataElement.dataset.idmeet;
let notifiedUsers = {};  
let wakeLock = null;
let loggedInUser = userName;
let loggedInUserId = userDataElement.dataset.loggedInUserId;


document.addEventListener("DOMContentLoaded", function () {
    locationsList = document.getElementById('locations-list');
    const userForm = document.getElementById('user-form');
    const formContainer = document.getElementById('form-container');
    const content = document.getElementById('content');
    if (!userName || !userColor || !refreshInterval || !termsAccepted) {
        formContainer.style.display = 'block';
        content.style.display = 'none';
    } else {
        formContainer.style.display = 'none';
        content.style.display = 'flex';
    }

    userForm.addEventListener('submit', function (event) {
        event.preventDefault();
        userColor = document.getElementById('color').value;
        refreshInterval = parseInt(document.getElementById('refresh-interval').value) * 1000;
        const termsAccepted = document.getElementById('terms').checked;
        if (userColor && refreshInterval && termsAccepted) {
            formContainer.style.display = 'none';
            content.style.display = 'flex';
            initMap();
        } else {
            alert('Por favor, complete todos los campos y acepte los términos y condiciones.');
        }
    });

    window.addEventListener('beforeunload', function () {
        if (navigator.geolocation) {
            navigator.geolocation.clearWatch(watchId);
        }
        disconnectClient();
    });

    function initMap() {
        requestWakeLock();
        navigator.permissions.query({ name: 'geolocation' }).then(function (result) {
            if (result.state === 'granted') {
                console.log('Geolocalización habilitada');
            } else if (result.state === 'prompt') {
                console.log('El usuario necesita activar la geolocalización.');
            } else if (result.state === 'denied') {
                console.log('Geolocalización denegada.');
            }
        });
        const mapOptions = {
            center: { lat: 0, lng: 0 },
            zoom: 2
        };
        map = new google.maps.Map(document.getElementById('map'), mapOptions);
        const points = JSON.parse(mapDataElement.dataset.points);  
        console.log(points);
        points.forEach(function (point) {
            const position = { lat: parseFloat(point.lat), lng: parseFloat(point.lng) };
            const marker = new google.maps.Marker({
                map: map,
                position: position,
                title: point.name,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 10,
                    fillColor: "#00FF00",  
                    fillOpacity: 1,
                    strokeWeight: 1,
                    strokeColor: '#000'
                }
            });

            console.log("POINT - ", point);
            console.log("ID PREGUNTAAAA", point.idPregunta_id);
            console.log(point);
            const circle = new google.maps.Circle({
                map: map,
                center: position,
                radius: parseFloat(point.radius),  
                strokeColor: "#FF0000",
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: "#FF0000",
                fillOpacity: 0.35,
                enlace: point.enlace,
                idPregunta: point.idPregunta_id,
                tipoEvento: point.tipoEvento,
                valor: point.valor
            });

            console.log(circle);
            markers[point.name] = marker;
            circles[point.name] = circle;
            const infoWindow = new google.maps.InfoWindow({
                content: `<h5>${point.name}</h5><p>${point.description}</p>`
            });

            marker.addListener('click', function () {
                Object.values(infoWindows).forEach(iw => iw.close());
                infoWindow.open(map, marker);
            });
            infoWindows[point.name] = infoWindow;
        });
        updateUserLocation();
        setInterval(updateUserLocation, refreshInterval);
    }


    function updateUserLocation() {
        fetch(`/get_user_location/${loggedInUserId}`)
            .then(response => response.json())
            .then(data => {
                if (data.lat && data.lng) {
                    const userPosition = new google.maps.LatLng(data.lat, data.lng);
                    if (markers['userLocation'] && circles['userLocation']) {
                        markers['userLocation'].setPosition(userPosition);
                        circles['userLocation'].setCenter(userPosition);
                    } else {
                        const userMarker = new google.maps.Marker({
                            position: userPosition,
                            map: map,
                            title: 'Tu ubicación',
                            icon: {
                                path: google.maps.SymbolPath.CIRCLE,
                                scale: 10,
                                fillColor: '#FF0000',
                                fillOpacity: 1,
                                strokeWeight: 1,
                                strokeColor: '#000'
                            }
                        });
                        const userCircle = new google.maps.Circle({
                            map: map,
                            center: userPosition,
                            radius: 0, 
                            strokeColor: "#0000FF",  
                            strokeOpacity: 0.8,
                            strokeWeight: 2,
                            fillColor: "#0000FF",  
                            fillOpacity: 0.35
                        });
                        map.setCenter(userPosition);
                        map.setZoom(12);  
                        markers['userLocation'] = userMarker;
                        circles['userLocation'] = userCircle;
                    }
                    checkIfUserInCircle(userPosition);
                }
            })
            .catch(error => console.error('Error al obtener la ubicación del usuario:', error));
    }


    function sendLocation(location) {
        fetch('/update_location/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(location)
        }).then(response => response.json())
            .then(data => {
                console.log(data);
            }).catch(error => {
                console.error('Error sending location', error);
            });
    }

    function fetchUserPoints() {
        console.log(`la ruta: /obtener_puntos_usuario/${idmeet}/`)
        fetch(`/obtener_puntos_usuario/${idmeet}/`) 
            .then(response => response.json())
            .then(data => {
                if (data.total_puntos !== undefined) {
                    const puntosElement = document.querySelector('#points-container .text-success');
                    const pointsContainer = document.querySelector('#points-container');
                    if (puntosElement.innerText !== `${data.total_puntos} pts`) {
                        puntosElement.classList.add('text-temporary-red');
                        pointsContainer.classList.add('vibrate');
                        setTimeout(() => {
                            puntosElement.classList.remove('text-temporary-red');
                            pointsContainer.classList.remove('vibrate');
                        }, 1000);
                    }
                    puntosElement.innerText = `${data.total_puntos} pts`;
                }
            })
            .catch(error => {
                console.error('Error fetching user points:', error);
            });
    }

    function fetchLocations() {
        fetch('/api/get_locationsApi/?idmeet=' + idmeet)
            .then(response => response.json())
            .then(data => {
                updateMarkers(data.locations);
                updateLocationsList(data.locations);
            })
            .catch(error => {
                console.error('Error fetching locations:', error);
            });
    }


    function updateMarkers(locations) {
        Object.values(markers).forEach(marker => marker.setMap(null));
        markers = {};
        infoWindows = {};

        locations.forEach(location => {
            if (location.name) {
                if (!markers[location.name]) {
                    const marker = new google.maps.Marker({
                        map: map,
                        position: { lat: location.lat, lng: location.lng },
                        title: location.name,
                        icon: {
                            path: google.maps.SymbolPath.CIRCLE,
                            scale: 10,
                            fillColor: location.color,
                            fillOpacity: 1,
                            strokeWeight: 1,
                            strokeColor: '#000'
                        }
                    });

                    const infoWindow = new google.maps.InfoWindow({
                        content: `<div>${location.name}</div>`
                    });

                    marker.addListener('click', () => {
                        // Close all other info windows
                        Object.values(infoWindows).forEach(iw => iw.close());
                        infoWindow.open(map, marker);
                    });

                    markers[location.name] = marker;
                    infoWindows[location.name] = infoWindow;
                } else {
                    // Update marker position if it already exists
                    markers[location.name].setPosition(new google.maps.LatLng(location.lat, location.lng));
                }
            }
        });
    }

    async function requestWakeLock() {
        try {
            wakeLock = await navigator.wakeLock.request('screen');
            console.log('Wake Lock activada.');
            wakeLock.addEventListener('release', () => {
                console.log('Wake Lock liberada.');
            });
        } catch (err) {
            console.error(`${err.name}, ${err.message}`);
        }
    }



    function updateLocationsList(locations) {
        // Clear the existing list
        locationsList.innerHTML = '';
        // Track the latest location for each client to avoid duplicates
        let latestLocations = {};
        locations.forEach(location => {
            if (location.name) {
                latestLocations[location.name] = location;
            }
        });
        Object.values(latestLocations).forEach((location, index, array) => {
            let distanceInfo = '';
            if (index > 0) {
                const prevLocation = array[index - 1];
                const distance = calculateDistance(prevLocation.lat, prevLocation.lng, location.lat, location.lng);
                distanceInfo = `<br><small>Distancia desde ${prevLocation.name}: ${distance.toFixed(2)} km</small>`;
            }

            const listItem = document.createElement('li');
            const lastUpdated = getLastUpdated(location.timestamp);
            listItem.innerHTML = `<strong>${location.name}</strong>: (${location.lat}, ${location.lng})<br><small>Last updated: ${lastUpdated}</small>${distanceInfo}`;
            listItem.addEventListener('click', () => {
                map.setCenter(new google.maps.LatLng(location.lat, location.lng));
                map.setZoom(10);  
            });
            locationsList.appendChild(listItem);
        });
    }

    function getLastUpdated(timestamp) {
        const now = new Date();
        const lastUpdate = new Date(timestamp);
        const diffInSeconds = Math.floor((now - lastUpdate) / 1000);

        if (diffInSeconds < 60) {
            return `${diffInSeconds} seconds ago`;
        } else if (diffInSeconds < 3600) {
            const minutes = Math.floor(diffInSeconds / 60);
            return `${minutes} minutes ago`;
        } else if (diffInSeconds < 86400) {
            const hours = Math.floor(diffInSeconds / 3600);
            return `${hours} hours ago`;
        } else {
            const days = Math.floor(diffInSeconds / 86400);
            return `${days} days ago`;
        }
    }


    function checkIfUserInCircle(userLatLng) {
        Object.keys(circles).forEach(circleName => {
            const circle = circles[circleName];
            const circleCenter = circle.getCenter();
            const circleRadius = circle.getRadius();  
            console.log(circle);
            const distance = google.maps.geometry.spherical.computeDistanceBetween(userLatLng, circleCenter);
            if (distance <= circleRadius && circleName != 'userLocation') {
                const notificationKey = `userLocation-${circleName}`;
                if (!notifiedUsers[notificationKey]) {
                    const alertSound = document.getElementById('alert-sound');
                    alertSound.play();
                    if (circle.tipoEvento === 'video') {
                        console.log(circle.valor)
                        createObjective(loggedInUser, idmeet, circleName, circle.valor);
                        showModal(circleName, circle.enlace);
                    } else if (circle.tipoEvento === 'pregunta') {
                        console.log(circle)
                        console.log(circle.idPregunta);
                        fetchQuestionAndShowModal(circleName, circle.idPregunta);
                    }
                    notifiedUsers[notificationKey] = true;
                }
            }
        });
    }

    function fetchQuestionAndShowModal(circleName, idPregunta) {
        fetch(`/get_question/${idPregunta}/`)
            .then(response => response.json())
            .then(data => {
                showQuestionModal(circleName, data.pregunta, data.respuestaCorrecta, data.respuestaErronea, data.puntuacionCorrecta, data.puntuacionIncorrecta);
            })
            .catch(error => {
                console.error('Error al obtener la pregunta:', error);
            });
    }

    function showQuestionModal(circleName, pregunta, respuestaCorrecta, respuestaIncorrecta, puntuacionCorrecta, puntuacionIncorrecta) {
        document.getElementById('questionModalLabel').textContent = `Pregunta: ${circleName}`;
        document.getElementById('questionTexto').textContent = pregunta;
        const correctButton = document.getElementById('correctAnswerButton');
        const incorrectButton = document.getElementById('incorrectAnswerButton');
        correctButton.textContent = respuestaCorrecta;
        incorrectButton.textContent = respuestaIncorrecta;
        correctButton.onclick = function () {
            alert('Respuesta Correcta 🎉');
            createObjective(loggedInUser, idmeet, circleName, puntuacionCorrecta);
            $('#questionModal').modal('hide');
        };

        incorrectButton.onclick = function () {
            alert('Respuesta Incorrecta 😞');
            createObjective(loggedInUser, idmeet, circleName, puntuacionIncorrecta);
            $('#questionModal').modal('hide');
        };
        $('#questionModal').modal('show');
    }


    function showModal(circleName, enlace) {
        document.getElementById('modalLabel').textContent = `Punto de Interés: ${circleName}`;
        document.getElementById('modalEnlaceTexto').textContent = `Estás dentro del área de este punto de interés. Puedes hacer clic en el enlace para más información:`;
        enlaceYou = "https://www.youtube.com/watch?v=" + enlace;
        const enlaceButton = document.getElementById('enlaceButton');
        enlaceButton.href = enlaceYou;
        enlaceButton.style.display = enlace ? 'block' : 'none';
        const videoIframe = document.getElementById('videoIframe');
        enlaceEntero = "https://www.youtube.com/embed/" + enlace;
        videoIframe.src = enlaceEntero;
        $('#enlaceModal').modal('show');
    }


    function createObjective(userName, idmeet, concepto, valor) {
        fetch('/create_objective/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  
            },
            body: JSON.stringify({
                user_name: userName,
                idmeet: idmeet,
                concepto: concepto,
                valor: valor
            })
        }).then(response => response.json())
            .then(data => {
                console.log('Objetivo creado:', data);
                fetchUserPoints();
            }).catch(error => {
                console.error('Error al crear objetivo:', error);
            });
    }


    function checkIfUserInMostoles(location) {
        const userLatLng = new google.maps.LatLng(location.lat, location.lng);
        if (google.maps.geometry.poly.containsLocation(userLatLng, mostolesPolygon)) {
            alert(`El usuario ${location.name} está dentro del término municipal de Móstoles.`);
        }
    }


    function calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371;
        const dLat = degreesToRadians(lat2 - lat1);
        const dLon = degreesToRadians(lon2 - lon1);
        const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(degreesToRadians(lat1)) * Math.cos(degreesToRadians(lat2)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        const distance = R * c;
        return distance;
    }


    function degreesToRadians(degrees) {
        return degrees * (Math.PI / 180);
    }


    function disconnectClient() {
        fetch('/disconnect/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ name: userName })
        }).then(response => response.json())
            .then(data => {
                console.log('Disconnected:', data);
            }).catch(error => {
                console.error('Error disconnecting', error);
            });
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
});