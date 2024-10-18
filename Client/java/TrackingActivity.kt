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
package com.example.myapplication

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.os.Looper
import android.os.PowerManager
import android.util.Log
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationCallback
import com.google.android.gms.location.LocationRequest
import com.google.android.gms.location.LocationResult
import com.google.android.gms.location.LocationServices
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import com.example.myapplication.LocationRequestData

class TrackingActivity : AppCompatActivity() {

    private lateinit var startButton: Button
    private lateinit var stopButton: Button
    private lateinit var locationTextView: TextView
    private lateinit var fusedLocationClient: FusedLocationProviderClient
    private lateinit var locationRequest: LocationRequest
    private lateinit var locationCallback: LocationCallback
    private var tracking = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_tracking)
        val sharedPreferences = getSharedPreferences("prefs", MODE_PRIVATE)
        val batteryOptimizationAsked = sharedPreferences.getBoolean("battery_optimization_asked", false)

        if (!batteryOptimizationAsked) {
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
                val intent = Intent()
                val packageName = packageName
                val pm = getSystemService(POWER_SERVICE) as PowerManager
                if (!pm.isIgnoringBatteryOptimizations(packageName)) {
                    intent.action = android.provider.Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS
                    intent.data = Uri.parse("package:$packageName")
                    startActivity(intent)
                    sharedPreferences.edit().putBoolean("battery_optimization_asked", true).apply()
                }
            }
        }

        startButton = findViewById(R.id.startButton)
        stopButton = findViewById(R.id.stopButton)
        locationTextView = findViewById(R.id.locationTextView)
        val token = intent.getStringExtra("token")
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
        locationRequest = LocationRequest.create().apply {
            priority = LocationRequest.PRIORITY_HIGH_ACCURACY
            interval = 5000  // Intervalo de actualización de 5 segundos
            fastestInterval = 5000  // El intervalo de actualización más rápido permitido
        }

        locationCallback = object : LocationCallback() {
            override fun onLocationResult(locationResult: LocationResult) {
                for (location in locationResult.locations) {
                    val latitude = location.latitude
                    val longitude = location.longitude
                    updateLocationUI(latitude, longitude)
                    if (token != null) {
                        sendLocationToServer(latitude, longitude, token)
                    }
                }
            }
        }

        startButton.setOnClickListener {
            if (!tracking) {
                startLocationUpdates()
                tracking = true
                Toast.makeText(this, "Seguimiento iniciado", Toast.LENGTH_SHORT).show()
                val serviceIntent = Intent(this, TrackingService::class.java)
                startService(serviceIntent)
            }
        }

        stopButton.setOnClickListener {
            if (tracking) {
                stopLocationUpdates()
                tracking = false
                Toast.makeText(this, "Seguimiento detenido", Toast.LENGTH_SHORT).show()
                val serviceIntent = Intent(this, TrackingService::class.java)
                stopService(serviceIntent)
            }
        }
    }

    // Iniciar la actualización de la ubicación
    private fun startLocationUpdates() {
        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
                1
            )
            return
        }
        fusedLocationClient.requestLocationUpdates(locationRequest, locationCallback, Looper.getMainLooper())
    }

    private fun stopLocationUpdates() {
        fusedLocationClient.removeLocationUpdates(locationCallback)
    }

    private fun updateLocationUI(lat: Double, lng: Double) {
        locationTextView.text = "Ubicación actual: Latitud $lat, Longitud $lng"
    }

    private fun sendLocationToServer(lat: Double, lng: Double, token: String) {
        val idmeet2 = "d10f3a03648048e88ec5ef69bb7e0144"
        val locationRequest = LocationRequestData(lat, lng, idmeet2, token)

        RetrofitClient.apiService.updateLocation(locationRequest).enqueue(object : Callback<Void> {
            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                if (response.isSuccessful) {
                    Log.d("TrackingActivity", "Ubicación enviada al servidor exitosamente")
                } else {
                    Log.e("TrackingActivity", "Error enviando ubicación al servidor: ${response.code()}")
                }
            }

            override fun onFailure(call: Call<Void>, t: Throwable) {
                Log.e("TrackingActivity", "Error de conexión: ${t.message}")
            }
        })
    }
}
