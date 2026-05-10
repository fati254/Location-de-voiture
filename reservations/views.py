from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

from io import BytesIO
import qrcode
import os

from django.conf import settings

from .models import Reservation, Payment
from cars.models import Car , Notification

from django.contrib import messages

from datetime import date

# =========================
# LISTE RESERVATIONS
# =========================
@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user)
    
    return render(request, 'reservations/list.html', {
        'reservations': reservations
    })


# =========================
#  CREATE RESERVATION
# =========================
@login_required
def create_reservation(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")

        reservation = Reservation.objects.create(
            user=request.user,
            car=car,
            date_debut=date_debut,
            date_fin=date_fin,
            is_validated=True
        )
        Notification.objects.create(
            user=request.user,
            title="Réservation confirmée",
            message=f"Votre réservation pour {car.marque} {car.modele} a été effectuée avec succès."
        )

        Payment.objects.create(
            reservation=reservation,
            amount=500,
            status="pending"
        )

        return redirect('payment_page', reservation_id=reservation.id)

    return render(request, "reservations/create.html", {"car": car})


# =========================
#  SUCCESS
# =========================
@login_required
def reservation_success(request):
    return render(request, "reservations/success.html")


# =========================
# GENERATE CONTRACT PDF
# =========================
@login_required
def generate_contract(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    payment = get_object_or_404(Payment, reservation=reservation)

    # sécurité
    if payment.status != "paid":
        return HttpResponse(" Paiement requis pour générer le contrat")

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    y = 800

    # =========================
    # HEADER CENTRÉ
    # =========================
    title = "AUTOLUX - CONTRAT DE LOCATION"
    subtitle = "Plateforme officielle AutoLux"

    pdf.setFont("Helvetica-Bold", 18)
    title_width = pdfmetrics.stringWidth(title, "Helvetica-Bold", 18)
    pdf.drawString((600 - title_width) / 2, y, title)

    y -= 25

    pdf.setFont("Helvetica", 11)
    subtitle_width = pdfmetrics.stringWidth(subtitle, "Helvetica", 11)
    pdf.drawString((600 - subtitle_width) / 2, y, subtitle)

    y -= 20
    pdf.line(50, y, 550, y)

    y -= 40

    # =========================
    # CLIENT
    # =========================
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "INFORMATIONS CLIENT")
    y -= 20

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Client : {request.user.username}")

    y -= 40

    # =========================
    # LOCATION
    # =========================
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "DÉTAILS DE LA LOCATION")
    y -= 20

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Voiture : {reservation.car.marque} {reservation.car.modele}")
    y -= 20

    pdf.drawString(50, y, f"Date début : {reservation.date_debut}")
    y -= 20

    pdf.drawString(50, y, f"Date fin : {reservation.date_fin}")
    y -= 40

    # =========================
    # PRIX
    # =========================
    days = (reservation.date_fin - reservation.date_debut).days
    if days <= 0:
        days = 1

    prix_jour = reservation.car.prix_par_jour
    total = days * prix_jour

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "DÉTAILS DU PAIEMENT")
    y -= 20

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Prix par jour : {prix_jour} DH")
    y -= 20

    pdf.drawString(50, y, f"Nombre de jours : {days}")
    y -= 20

    pdf.drawString(50, y, f"Total payé : {total} DH")
    y -= 20

    pdf.drawString(50, y, "Statut : PAYÉ ✔")

    y -= 60

    # =========================
    # SIGNATURE (GAUCHE)
    # =========================
    pdf.line(50, y, 250, y)
    y -= 15

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, "Signature AutoLux")

    y -= 15
    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(50, y, "Responsable AutoLux")

    # =========================
    # FOOTER CENTRÉ
    # =========================
    footer1 = "AutoLux © 2026 - Tous droits réservés"
    footer2 = "Document officiel généré automatiquement"

    pdf.setFont("Helvetica", 8)

    footer1_width = pdfmetrics.stringWidth(footer1, "Helvetica", 8)
    footer2_width = pdfmetrics.stringWidth(footer2, "Helvetica", 8)

    pdf.drawString((600 - footer1_width) / 2, 50, footer1)
    pdf.drawString((600 - footer2_width) / 2, 35, footer2)

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="AutoLux_Contrat_{reservation.id}.pdf"'

    return response


# =========================
#  PAYMENT PAGE
# =========================
@login_required
def payment_page(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    payment = get_object_or_404(Payment, reservation=reservation)

    if request.method == "POST":
        action = request.POST.get("action")

        # PAIEMENT
        if action == "pay":
            payment.status = "paid"
            payment.save()
            Notification.objects.create(
              user=request.user,
              title="Paiement confirmé",
              message=f"Le paiement de votre réservation pour {reservation.car.marque} {reservation.car.modele} a été effectué avec succès."
     )

            return redirect("payment_success", reservation_id=reservation.id)

        # ANNULATION
        elif action == "cancel":
            payment.status = "cancelled"
            payment.save()
            Notification.objects.create(
             user=request.user,
             title="Réservation annulée",
             message=f"Votre réservation pour {reservation.car.marque} {reservation.car.modele} a été annulée."
)

            return redirect("cars_list")

    return render(request, "payment.html", {
        "reservation": reservation,
        "payment": payment
    })

@login_required
def payment_success(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    payment = get_object_or_404(Payment, reservation=reservation)

    return render(request, "payment_success.html", {
        "reservation": reservation,
        "payment": payment
    })

@login_required
def history(request):
    reservations = Reservation.objects.filter(user=request.user)
    payments = Payment.objects.filter(reservation__user=request.user)

    data = []

    for r in reservations:
        delay_days, penalty = calculate_penalty(r)

        data.append({
            "reservation": r,
            "delay_days": delay_days,
            "penalty": penalty
        })

    return render(request, "history.html", {
        "data": data,
        "payments": payments
    })


def calculate_penalty(reservation):
    today = date.today()

    if today > reservation.date_fin:
        delay_days = (today - reservation.date_fin).days

        prix_jour = reservation.car.prix_par_jour

        penalty = delay_days * prix_jour * 1.5  # coefficient

        return delay_days, penalty

    return 0, 0

@property
def number_of_days(self):

    return (
        self.date_fin - self.date_debut
    ).days

