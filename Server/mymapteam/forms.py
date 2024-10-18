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
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, PointOfInterest, Question

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile(user=user, email=self.cleaned_data['email'], phone=self.cleaned_data['phone'])
            profile.save()
        return user


from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'duration', 'idmeet', 'password']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'duration': forms.NumberInput(attrs={'min': 1, 'max': 8, 'type': 'number'}),
            'idmeet': forms.HiddenInput(),
            'password': forms.HiddenInput(),
        }

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration < 1 or duration > 8:
            raise forms.ValidationError("Duration must be between 1 and 8 hours")
        return duration

class PointOfInterestForm(forms.ModelForm):
    class Meta:
        model = PointOfInterest
        fields = ['name']  
