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
let marker;
let circle;
window.onload = function initMap() {
    const defaultLocation = { lat: 40.416775, lng: -3.703790 };  
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 6,
        center: defaultLocation
    });
    map.addListener('click', function (event) {
        placeMarker(event.latLng);
    });


    function placeMarker(location) {
        if (marker) {
            marker.setPosition(location);
        } else {
            marker = new google.maps.Marker({
                position: location,
                map: map
            });
        }
        document.getElementById('lat').value = location.lat();
        document.getElementById('lng').value = location.lng();
        if (circle) {
            circle.setMap(null);
        }
        drawCircle(location, parseFloat(document.getElementById('radius').value));
    }


    function drawCircle(location, radius) {
        circle = new google.maps.Circle({
            map: map,
            center: location,
            radius: radius,  
            strokeColor: document.getElementById('color').value,
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: document.getElementById('color').value,
            fillOpacity: 0.35
        });
    }

    document.getElementById('radius').addEventListener('input', function () {
        const radius = parseFloat(this.value);
        if (circle && marker) {
            circle.setRadius(radius);  
        }
    });
}

const colorOptions = document.querySelectorAll('.color-option');
const colorInput = document.getElementById('color');

colorOptions.forEach(option => {
    option.addEventListener('click', function () {
        colorOptions.forEach(opt => opt.classList.remove('selected'));
        this.classList.add('selected');
        colorInput.value = this.getAttribute('data-color');
    });
});


document.getElementById('tipoEvento').addEventListener('change', function () {
    const selectedType = this.value;
    document.getElementById('videoFields').style.display = selectedType === 'video' ? 'block' : 'none';
    document.getElementById('preguntaFields').style.display = selectedType === 'pregunta' ? 'block' : 'none';
});
