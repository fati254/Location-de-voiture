from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from cars.models import Car

@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user)

    return render(request, 'reservations/list.html', {
        'reservations': reservations
    })

#reserver une voiture
@login_required
def create_reservation(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")

        Reservation.objects.create(
            user=request.user,
            car=car,
            date_debut=date_debut,
            date_fin=date_fin
        )
         #succes
        return redirect("reservation_success")

    return render(request, "reservations/create.html", {"car": car})

#reservation passer avec succes
@login_required
def reservation_success(request):
    return render(request, "reservations/success.html")