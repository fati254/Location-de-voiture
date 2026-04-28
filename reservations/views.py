from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Reservation
from cars.models import Car 

@login_required
def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/list.html', {'reservations' : reservations})


def reservation_list(request):
    cars = Car.objects.all()   # récupérer voitures

    return render(request, 'reservations/list.html', {
        'cars': cars
    })